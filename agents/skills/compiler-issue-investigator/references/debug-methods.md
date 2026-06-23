# Compiler Debug Methods

Use this file only when choosing concrete investigation techniques.

## General Pattern

Record the full command first, then add one source of observability at a time. Prefer smaller IR or source inputs over larger logs. Preserve both a failing and a nearby passing case when possible.

## Triton

- Capture Python package version, CUDA/ROCm version, GPU name, driver, and relevant environment variables.
- Save generated TTIR, TTGIR, LLVM IR, PTX/AMDGPU, and final kernel artifacts when available.
- Try boundary changes: tensor shape, dtype, num warps, num stages, block size, layout, target backend, and optimization flags.
- Separate frontend semantic issues from lowering/codegen/runtime issues by checking whether failure appears before or after IR generation.

## MLIR

- Use pass dumps, verifier output, crash reproducers, and reduced `.mlir` files.
- Preserve the exact pass pipeline and dialect versions.
- Narrow the first pass that introduces invalid IR by comparing before/after dumps.
- If using `mlir-reduce`, keep the original failing module and the reducer predicate command.

## LLVM

- Reduce toward `.ll` or `.mir` when the bug is in optimization, instruction selection, register allocation, or backend emission.
- Use `opt`, `llc`, and verifier checks to split optimizer vs backend behavior.
- Capture pass remarks, pass pipelines, target triple, data layout, CPU, features, and relocation/code model flags.
- For miscompiles, keep an executable oracle: expected output, actual output, and the smallest input that distinguishes them.

## Clang

- Prefer a `clang -cc1` repro when possible; save the command produced by `clang -###`.
- Capture preprocessed source with `-E` or minimized source with the exact language standard, target, include paths, and macros.
- Split frontend diagnostics, AST/Sema, IR generation, optimizer, and backend by preserving AST/LLVM IR outputs.

## Root Cause Evidence

Strong evidence usually includes one of:

- first bad pass or commit
- minimal IR/source that fails
- exact source line or function implementing the wrong transformation
- invariant violation with verifier/assertion/log support
- side-by-side before/after IR showing the incorrect change
- patch sketch or local experiment that changes the observed behavior

