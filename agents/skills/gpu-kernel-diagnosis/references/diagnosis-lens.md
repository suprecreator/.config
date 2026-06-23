# GPU Kernel Diagnosis Lens

用这个参考文档把零散底层概念归到少数几个可观察关注点。

更深入诊断时，只加载匹配当前瓶颈的单个参考文档：

| 参考文档 | 主题 |
|---|---|
| `effective-work.md` | Vec1、predicate、mask、active lane、overfetch |
| `memory-efficiency.md` | vec4 ld/st、coalescing、alignment、cache policy |
| `dependency-chain.md` | RAW、ALU forwarding、load-use dependency |
| `parallel-degree.md` | TLP、ILP、MLP、occupancy、latency hiding |
| `resource-pressure.md` | register、spill、local memory、shared memory |
| `issue-efficiency.md` | dual issue、uniform datapath、pipe utilization |

## 关注点总表

| 关注点 | 它问什么 | 常见收益 | 常见失败 | 证据 |
|---|---|---|---|---|
| 有效工作量 | 发出的工作有多少真的有用？ | Vec1 标量化、更好 mask、避免 overfetch | predicate 稀疏、用 vec4 搬 vec1 数据、inactive lane 多 | active lane、predicate density、useful bytes/request |
| 访存效率 | memory op 是否足够宽、对齐、合并，并且复用策略正确？ | vec2/vec4 ld/st、coalescing、cache policy、shared memory tiling | misalignment、gather/scatter、cache pollution、tail overfetch | PTX ld/st 形式、SASS LDG/STG 宽度、sectors/request、bandwidth |
| 依赖链 | 指令是否被 RAW 依赖串行化？ | 打断地址链、重排独立工作、ALU forwarding | 长 IADD/IMAD 链、load-use 链、tensor result dependency | SASS register dependency、scoreboard stall |
| 并行度 | 有多少独立工作可以隐藏延迟？ | 更多 resident warp、ILP、MLP、software pipelining | occupancy 不足、outstanding load 太少、loop-carried dependency | occupancy、eligible warps、memory latency stall |
| 资源压力 | kernel 是否装得下机器资源？ | 缩短 live range、减少临时 vector、减少 shared memory | register spill、occupancy 下降、shared memory 限制 CTA 数 | ptxas registers、shared memory bytes、local memory、LDL/STL |
| 发射效率 | scheduler 是否能持续发出有用指令？ | dual issue、uniform datapath、pipe balance | pipe conflict、operand source conflict、dependency gap | issue slot utilization、pipe utilization、SASS mix |

## Vec1、Vec4 和 Spill

Vec1 是计算粒度。它让每个 lane 只持有标量值，live range 可以独立结束，通常有利于 DCE 和减少强制分量浪费。

vec4 load/store 是访存粒度。它可以减少访存指令数并提高宽访存机会，但 128-bit load 仍然需要寄存器承载结果，通常是多个 32-bit register。如果 4 个元素长时间同时活着，register pressure 会增加。

使用规则：

```text
访存边界使用 vec4
计算内部保持 scalar/vec1
load 到 store 之间缩短 live range
```

## RAW 和 Forwarding

RAW 依赖不会因为 forwarding 消失。Forwarding 只是让 consumer 在结果写回并重新读寄存器前，就从 bypass path 拿到 ALU 结果。

不好的地址形态：

```text
addr1 = base + off
addr2 = addr1 + 4
addr3 = addr2 + 4
```

更好的地址形态：

```text
addr1 = base + off1
addr2 = base + off2
addr3 = base + off3
```

第二种形式暴露更多 ILP，因为多个地址共享 base，但彼此不依赖。

## Dual-Issue 检查

更可能 dual issue 的情况：

- 指令彼此独立；
- execution pipe 兼容；
- operand source 没有压爆同一条读取路径；
- scheduler 有足够 ready warp 或 ready instruction。

不容易 dual issue 的情况：

- B 指令消费 A 指令结果；
- 两条指令竞争同一受限 pipeline；
- register bank/read-port 压力高；
- warp 正在等 memory 或 barrier。

## 证据清单

比较两个 kernel 优化版本时，收集：

```text
source version A/B
benchmark timing
PTX memory instruction form
SASS memory instruction form
ptxas register count
local memory / spill evidence
occupancy
Nsight bandwidth
Nsight sectors/request or memory transactions
Nsight dependency / scoreboard / issue stalls
```

解释必须覆盖两边：

```text
为什么这个优化理论上会有收益
为什么它在当前 kernel 上可能失败
哪个观察结果能决定结论
```
