# 发射效率

用于诊断 dual issue、scheduler utilization、uniform datapath、operand source 和 pipe balance。

## 核心问题

```text
scheduler 是否能持续发出有用指令，并把兼容工作配对？
```

## Dual-Issue 条件

更可能 dual issue 的情况：

```text
instructions are independent
execution pipes are compatible
operand sources do not conflict heavily
there are enough ready instructions or ready warps
```

dual issue 被阻塞或削弱的情况：

```text
instruction B consumes instruction A's result
both instructions need the same constrained pipe
register read/bank pressure is high
warp is stalled on memory/barrier/dependency
```

## Uniform Datapath

当一个值对整个 warp/program 相同，uniform datapath/registers 可能有用：

```text
base = program_id * BLOCK
addr = base + per_lane_offset
```

把公共计算和 per-lane 计算写清楚，让编译器更容易选择高效表示。

## 证据

收集：

```text
SASS instruction mix
pipe utilization
issue slot utilization
eligible warps per scheduler
register operand sources: R, UR, c[]
dependency stalls
```

## 实用规则

不要孤立追求 dual issue。先让 instruction stream 有足够独立性，再检查 pipe balance 和 operand source 是否允许更好的 issue 行为。
