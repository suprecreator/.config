# 有效工作量

当问题是“发出去的工作到底有多少真的有用”时，使用这个视角。

## 核心问题

```text
执行的 lane、vector slot、memory byte 有多少产生了有效结果？
```

## 常见信号

| 主题 | 要检查什么 | 失败形态 |
|---|---|---|
| Vec1/scalar execution | 操作是否天然是每个 lane 一个标量？ | 被迫使用 vec4，但部分分量无用。 |
| Predicate/mask | 有多少 lane 或元素 active？ | mask 稀疏，指令发出但有效 lane 很少。 |
| Tail handling | 尾部 partial tile 多大？ | vec4 大部分元素是 invalid tail。 |
| Overfetch | load 的字节是否都被消费？ | 宽 load 搬了后续不用的数据。 |

## 诊断规则

```text
active lane/element 密集时，vectorized memory work 更可能有利。
mask 稀疏或 tail 占比高时，vectorization 可能浪费工作。
```

## 证据

收集：

```text
mask expression
problem sizes and tail size
active lane or predicate density if available
useful bytes vs requested bytes
PTX/SASS predicated load/store shape
benchmark for aligned/full case vs tail-heavy case
```

## 实用规则

计算保持 scalar；只有当 vector 元素基本都会被使用时，才在访存边界使用 vectorized load/store。
