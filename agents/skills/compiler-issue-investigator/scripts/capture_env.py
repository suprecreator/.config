#!/usr/bin/env python3
import argparse
import os
import platform
import shutil
import subprocess
from pathlib import Path


TOOLS = [
    ["git", "--version"],
    ["python3", "--version"],
    ["clang", "--version"],
    ["clang++", "--version"],
    ["mlir-opt", "--version"],
    ["mlir-translate", "--version"],
    ["opt", "--version"],
    ["llc", "--version"],
    ["llvm-dis", "--version"],
    ["llvm-reduce", "--version"],
    ["ptxas", "--version"],
    ["nvcc", "--version"],
]


def run(cmd: list[str]) -> str:
    if shutil.which(cmd[0]) is None:
        return f"$ {' '.join(cmd)}\n<not found>\n"
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return f"$ {' '.join(cmd)}\n{proc.stdout.strip()}\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture compiler investigation environment.")
    parser.add_argument("--case-dir", required=True)
    args = parser.parse_args()

    case_dir = Path(args.case_dir).resolve()
    out = case_dir / "runs" / "environment"
    out.mkdir(parents=True, exist_ok=True)

    lines = [
        f"platform: {platform.platform()}",
        f"machine: {platform.machine()}",
        f"python: {platform.python_version()}",
        f"cwd: {Path.cwd()}",
        "",
        "## selected environment",
    ]
    for key in sorted(os.environ):
        if key.startswith(("LLVM", "MLIR", "TRITON", "CUDA", "ROCM", "HIP", "CC", "CXX")) or key in {
            "PATH",
            "LD_LIBRARY_PATH",
            "DYLD_LIBRARY_PATH",
        }:
            lines.append(f"{key}={os.environ[key]}")

    lines.append("\n## tool versions")
    for cmd in TOOLS:
        lines.append(run(cmd))

    (out / "env.txt").write_text("\n".join(lines))
    print(out / "env.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

