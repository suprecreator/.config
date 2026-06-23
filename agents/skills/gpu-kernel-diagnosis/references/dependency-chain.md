# 依赖链

用于诊断 RAW dependency、ALU forwarding、load-use latency 和地址生成串行化。

## 核心问题

```text
后续指令是否因为消费前面指令结果而等待？
```

## 依赖类型

| 类型 | 例子 | 改法 |
|---|---|---|
| ALU RAW | `R2 = R1 + 4` 紧跟 `R1 = ...` | 重排独立工作；改写成更容易暴露 ILP 的形式。 |
| 地址链 | `addr2 = addr1 + 4` | 从共同 base 并行计算多个地址。 |
| Load-use | `x = load(addr); y = x + 1` | 插入独立工作、prefetch 或 pipeline。 |
| Loop-carried | 下一轮依赖上一轮结果 | unroll、pipeline，必要时改算法。 |

## Forwarding

ALU forwarding 通过绕过 register-file writeback/readback 来缩短 ALU RAW latency。它不消除依赖。

```text
无 forwarding：produce -> writeback -> register read -> consume
有 forwarding：produce -> bypass path -> consume
```

Forwarding 对 ALU-to-ALU 链有用，但不解决 global memory load latency。

## 证据

收集：

```text
SASS instruction sequence
producer and consumer registers
scoreboard/dependency stall metrics
load-use distance
loop body dependency structure
```

## 实用规则

优先使用独立地址和 ALU 表达式：

```text
bad:  addr1 = base + off; addr2 = addr1 + 4; addr3 = addr2 + 4
good: addr1 = base + off1; addr2 = base + off2; addr3 = base + off3
```
