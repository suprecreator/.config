#!/usr/bin/env python3
import argparse
import datetime as dt
import os
import shutil
import subprocess
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]


def git_value(repo: Path, args: list[str]) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a compiler investigation case directory.")
    parser.add_argument("--case-dir", required=True)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--problem", default="Compiler issue under investigation.")
    parser.add_argument("--slug", default="")
    args = parser.parse_args()

    case_dir = Path(args.case_dir).resolve()
    repo_root = Path(args.repo_root).resolve()
    slug = args.slug or case_dir.name
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")

    for rel in [
        "problem",
        "tests/original",
        "tests/minimized",
        "tests/expected",
        "runs",
        "analysis",
        "reports",
        "export",
    ]:
        (case_dir / rel).mkdir(parents=True, exist_ok=True)

    makefile = (SKILL_DIR / "assets/case-template/Makefile").read_text()
    makefile = makefile.replace("__SKILL_DIR__", str(SKILL_DIR))
    (case_dir / "Makefile").write_text(makefile)

    commit = git_value(repo_root, ["rev-parse", "HEAD"])
    remote = git_value(repo_root, ["remote", "get-url", "origin"])
    problem_block = "\n".join(f"  {line}" for line in args.problem.splitlines())
    manifest = f"""case_slug: {slug}
created_at: {now}
status: initialized
problem: |-
{problem_block}
repo_root: {repo_root}
git_commit: {commit}
git_remote: {remote}
primary_report: reports/report.html
ai_report: reports/report.md
"""
    (case_dir / "manifest.yaml").write_text(manifest)

    statement = f"""# Problem Statement

## Symptom

{args.problem}

## Expected Behavior

TODO

## Actual Behavior

TODO

## Reproduction Command

TODO

## Success Criteria

TODO
"""
    (case_dir / "problem/statement.md").write_text(statement)

    placeholders = {
        "analysis/timeline.md": "# Timeline\n\n",
        "analysis/hypotheses.md": "# Hypotheses\n\n",
        "analysis/debug-methods.md": "# Debug Methods\n\n",
        "analysis/findings.md": "# Findings\n\n",
        "analysis/code-links.md": "# Code Links\n\n",
    }
    for rel, content in placeholders.items():
        path = case_dir / rel
        if not path.exists():
            path.write_text(content)

    print(f"Initialized compiler investigation case: {case_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
