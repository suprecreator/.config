# 资源压力

用于诊断 register pressure、spill、local memory、shared memory 限制和 occupancy cliff。

## 核心问题

```text
这个优化是否消耗了过多硬件资源，反过来降低性能？
```

## 常见资源

| 资源 | 影响什么 | 失败形态 |
|---|---|---|
| Register | occupancy 和 spill | vec4 临时值或长 live range 增加 register count。 |
| Local memory | spill traffic | SASS 出现 `LDL`/`STL`，Nsight local memory traffic 上升。 |
| Shared memory | CTA residency 和 bank behavior | resident CTA 变少或出现 bank conflict。 |
| Constant/uniform value | 重复 per-lane work | 本可 uniform 的值占用普通 per-lane register。 |

## Spill

Register spill 表示原本希望留在 register 的值被放进 local memory。Local memory 逻辑上每线程私有，但物理上走 global memory/cache 路径。

除非 benchmark 明确证明无害，否则把 spill 当成严重警告。

## 证据

收集：

```text
ptxas register count
shared memory usage
occupancy calculation
SASS LDL/STL
Nsight local load/store metrics
benchmark before/after
```

## 实用规则

对 vec4 load/store，缩短 live range：

```text
load wide
consume soon
store soon
avoid keeping multiple vec4 groups live together
```
