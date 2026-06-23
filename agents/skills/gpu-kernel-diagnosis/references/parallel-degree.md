# 并行度

用于诊断 kernel 是否有足够独立工作隐藏延迟。

## 核心问题

```text
TLP、ILP、MLP 是否足够覆盖慢操作的 latency？
```

## 三种并行度

| 形式 | 含义 | 证据 |
|---|---|---|
| TLP | resident warp/CTA 带来的 thread/warp-level parallelism | occupancy、active warps、eligible warps |
| ILP | 单个 warp 内部的 independent instructions | SASS 中独立 ALU/address ops |
| MLP | 多个 outstanding memory operations | memory pipeline utilization、load concurrency |

## 解释规则

High occupancy 不自动等于好。只有当 kernel latency-bound，且更多 resident warp 可以在其他 warp 等待时运行，occupancy 才直接有用。

Low occupancy 不自动等于坏。如果每个 warp 有足够 ILP/MLP，或 kernel 受某个 throughput pipe 限制，中等 occupancy 也可能更快。

## 证据

收集：

```text
occupancy
eligible warps per scheduler
active warps per scheduler
stall reasons
load latency and outstanding memory behavior
loop unroll or software pipeline structure
register count and shared memory usage
```

## 实用规则

根据瓶颈选择需要的并行度：

```text
memory latency -> TLP and MLP
ALU dependency -> ILP
pipeline throughput -> enough ready independent instructions
resource-limited occupancy -> only reduce registers/shared memory if latency hiding is the issue
```
