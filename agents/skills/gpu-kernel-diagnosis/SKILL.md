---
name: gpu-kernel-diagnosis
description: Diagnose GPU kernel optimization bottlenecks for Triton, CUDA, PTX, SASS, Nsight Compute, vectorized load/store, register pressure, warp execution, cache policy, dual issue, ALU dependencies, and occupancy. Use when Codex needs to explain or debug low-level GPU performance behavior, compare vec1/vec2/vec4 implementations, build an evidence-based optimization checklist, or turn scattered architecture concepts into a concrete diagnosis.
---

# GPU Kernel Diagnosis

## 核心规则

不要按术语诊断，要按证据诊断。每个优化点都先归类到一个或多个可观察关注点：

| 关注点 | 关键问题 | 证据 |
|---|---|---|
| 有效工作量 | lane、vector slot、内存字节有没有浪费？ | active mask、tail 大小、predicate 密度、overfetch |
| 访存效率 | 访问是否连续、对齐、足够宽、可合并？ | PTX vector ld/st、SASS LDG/STG 宽度、sectors/request、带宽 |
| 依赖链 | RAW 链是否让执行串行化？ | 连续依赖的 IADD/IMAD/FFMA、scoreboard/dependency stall |
| 并行度 | 是否有足够 TLP、ILP、MLP 隐藏延迟？ | occupancy、独立指令、outstanding memory ops |
| 资源压力 | 优化是否增加 register、shared memory、local memory 压力？ | ptxas register count、occupancy、SASS LDL/STL、local memory 指标 |
| 发射效率 | 指令是否能配对并喂满不同 pipeline？ | dual issue 机会、operand source、pipe utilization |

## 工作流

1. 先说明讨论层级：Triton 源码、Triton IR/MLIR、PTX、ptxas、SASS、SM 执行、memory hierarchy 或 Nsight 指标。
2. 用上面的关注点表给优化点归类。
3. 说明预期收益和主要失败模式。
4. 有材料时按这个顺序看证据：源码片段、编译参数、PTX、SASS、ptxas register count、Nsight Compute 指标、benchmark 结果。
5. 输出短诊断：机制、下一步要检查什么、通过/失败标准。

## 常见映射

| 主题 | 主要关注点 | 诊断含义 |
|---|---|---|
| Vec1/scalar execution | 有效工作量 | 让每个 lane 的计算保持独立，避免被迫使用 vec4 分量。 |
| Predicate/mask | 有效工作量 | 控制哪些 lane 或元素生效；mask 稀疏会降低有效工作比例。 |
| vec4 ld/st | 访存效率 | 只有在数据连续、对齐、mask 密集、live range 不过长时才稳定有利。 |
| Cache policy | 访存效率 | 根据复用情况选择缓存策略；错误策略会污染 cache 或错过复用。 |
| Uniform datapath/registers | 资源压力、发射效率 | warp/program 公共计算应尽量避免重复放到 per-lane 路径。 |
| Register spill | 资源压力 | local memory 流量通常是危险信号，除非 benchmark 明确证明无害。 |
| ALU forwarding | 依赖链 | 缩短 ALU RAW 等待；不消除依赖，也不解决 memory latency。 |
| Dual issue | 发射效率 | 需要独立指令、兼容 pipeline、可接受的 operand/register-bank 压力。 |
| Occupancy | 并行度 | 只有当 kernel 需要更多 resident warp 隐藏延迟时才是目标。 |

## Triton Vec4 Load/Store 检查

诊断 Triton vectorized load/store 时，检查：

1. 地址模式是否连续且最好对齐：`base + {0,1,2,3} * sizeof(T)`。
2. PTX 是否出现预期的 vectorized memory op，例如 `ld.global.v4` 或等价形式。
3. SASS 是否出现预期宽访存，例如 16-byte 访问对应 `LDG/STG.128`。
4. register count 是否没有明显上涨到降低有效 occupancy 或导致 spill。
5. SASS 是否没有异常 `LDL`/`STL` local memory spill。
6. Nsight Compute 的 bandwidth、sectors/request、stall reason 是否朝预期方向变化。
7. tail mask 和 irregular indexing 是否把 vec4 变成 overfetch。

## 回答格式

诊断类回答使用这个紧凑结构：

```text
结论：
<一句话>

机制：
<按层级解释原因>

要查的证据：
<PTX/SASS/Nsight/register-count 项>

风险：
<这个优化最可能失败的方式>

下一个实验：
<一个具体对比实验>
```

## 参考文档

只加载当前瓶颈需要的参考文档：

| 参考文档 | 使用场景 |
|---|---|
| `references/diagnosis-lens.md` | 需要总表、总索引或快速定位关注点。 |
| `references/effective-work.md` | 诊断 Vec1、predicate、mask、lane utilization、overfetch。 |
| `references/memory-efficiency.md` | 诊断 vec2/vec4 ld/st、alignment、coalescing、cache policy、bandwidth。 |
| `references/dependency-chain.md` | 诊断 RAW、forwarding、load-use latency、地址生成串行化。 |
| `references/parallel-degree.md` | 诊断 TLP、ILP、MLP、occupancy、latency hiding、software pipelining。 |
| `references/resource-pressure.md` | 诊断 register pressure、spill、local memory、shared memory 限制、occupancy cliff。 |
| `references/issue-efficiency.md` | 诊断 dual issue、pipe utilization、uniform datapath、operand source、scheduler efficiency。 |
