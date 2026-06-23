# 访存效率

用于诊断 vec2/vec4 load/store、cache policy、alignment、coalescing 和 bandwidth。

## 核心问题

```text
memory operation 是否连续、对齐、足够宽、可合并，并且复用策略正确？
```

## 常见信号

| 主题 | 要检查什么 | 失败形态 |
|---|---|---|
| vec4 ld/st | PTX/SASS 是否真的出现宽访存？ | 源码 vectorized，但后端 scalarized。 |
| Alignment | base address 是否满足访问宽度对齐？ | 宽访问被拆成多个 transaction。 |
| Coalescing | 相邻 lane 是否访问相邻地址？ | gather/scatter 导致 sector 效率差。 |
| Cache policy | 数据在所选 cache level 是否有复用？ | L1 pollution，或 bypass 后错过复用。 |
| Store behavior | store 是否连续且完整？ | partial store 或 mask 降低 store 效率。 |

## 证据

收集：

```text
address formula
dtype and vector width
alignment guarantee
PTX ld.global/st.global form
SASS LDG/STG width
Nsight bandwidth
sectors/request or memory transaction metrics
cache hit rates where relevant
```

## Triton Vec4 通过标准

```text
通过：SASS 变成更宽的 memory op，bandwidth 变好，没有明显 register/spill 回退。
失败：source vectorization 没有保留到 SASS，或宽访问造成 overfetch、split transaction、spill。
```

## 实用规则

只有当地址接近 `base + {0,1,2,3} * sizeof(T)`，且大部分元素会被消费时，才优先做 vec4 memory access。
