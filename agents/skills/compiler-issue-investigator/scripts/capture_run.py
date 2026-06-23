#!/usr/bin/env python3
import argparse
import datetime as dt
import json
import os
import subprocess
import time
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a command and capture logs for an investigation case.")
    parser.add_argument("--case-dir", required=True)
    parser.add_argument("--run-id", default="")
    parser.add_argument("--shell", default="", help="Run this command string through bash -lc.")
    parser.add_argument("--shell-env", default="", help="Read a command string from this environment variable and run it through bash -lc.")
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()

    command = args.command
    command_display = ""
    shell_text = args.shell
    if args.shell_env:
        shell_text = os.environ.get(args.shell_env, "")
    if shell_text:
        command = ["bash", "-lc", shell_text]
        command_display = shell_text
    else:
        if command and command[0] == "--":
            command = command[1:]
        command_display = " ".join(command)
    if not command:
        raise SystemExit("missing command after --")

    run_id = args.run_id or dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = Path(args.case_dir).resolve() / "runs" / run_id
    artifacts = run_dir / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    (run_dir / "cmd.sh").write_text("#!/usr/bin/env bash\nset -euo pipefail\n" + command_display + "\n")
    env_subset = {
        k: v
        for k, v in os.environ.items()
        if k in {"PATH", "PWD", "HOME", "SHELL"} or k.startswith(("LLVM", "MLIR", "TRITON", "CUDA", "ROCM", "HIP"))
    }
    (run_dir / "env.txt").write_text("\n".join(f"{k}={env_subset[k]}" for k in sorted(env_subset)) + "\n")

    started = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    t0 = time.time()
    proc = subprocess.run(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    duration = time.time() - t0

    (run_dir / "stdout.log").write_text(proc.stdout)
    (run_dir / "stderr.log").write_text(proc.stderr)
    metadata = {
        "run_id": run_id,
        "started_at": started,
        "duration_seconds": round(duration, 3),
        "exit_code": proc.returncode,
        "command": command_display,
        "cwd": str(Path.cwd()),
        "artifacts": str(artifacts),
    }
    (run_dir / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n")
    print(f"captured run {run_id} exit={proc.returncode} at {run_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
