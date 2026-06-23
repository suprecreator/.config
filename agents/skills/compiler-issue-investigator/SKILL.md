---
name: compiler-issue-investigator
description: Systematic compiler issue investigation for Triton, LLVM, MLIR, Clang, codegen, optimizer, IR lowering, backend, or build/test regressions. Use when Codex needs to reproduce a compiler problem, write a minimal triggering case, run local or remote validation in isolated worktrees, delegate Triton/u22 remote execution to the triton-remote-dev runner, capture logs and debug commands under numbered artifacts, avoid pre-validation CI pushes, preserve experimental worktree cleanliness with stash/cleanup hygiene, handle concurrent agent validation safely, inspect IR/assembly/pass behavior, identify or narrow root cause, or package investigation artifacts for a dependency owner.
---

# Compiler Issue Investigator

## Core Contract

Investigate compiler problems as a reproducible research case, not as an ad hoc chat answer.

Always produce or update a case directory under `artifacts/<slug>` with a flat reading surface at the artifact root:

- flat, numbered reading files at the case root (`00-README.md`, `01-problem.md`, `02-code-path.md`, ...)
- a reading order that mirrors the investigation method and reasoning process
- minimal and original repro inputs, scripts, or code snippets when useful
- captured commands, stdout, stderr, environment, versions, and artifacts under raw-evidence subdirectories
- concise root-cause notes with hypotheses, eliminations, and exact evidence
- backend/handoff validation code when blocked by an external dependency owner
- an export bundle only when a packaged handoff is needed

Do **not** leave final investigation material under `investigations/`. If a temporary `investigations/<slug>` staging directory is created by habit or tooling, migrate the useful files into `artifacts/<slug>` and delete the staging directory before finishing.

## Quick Start

When starting a new case, create a flat case directory:

```bash
mkdir -p artifacts/<slug>/{runs,tests,export}
```

Create numbered root files immediately, even if short:

```text
artifacts/<slug>/00-README.md
artifacts/<slug>/01-problem.md
artifacts/<slug>/02-code-path.md
artifacts/<slug>/03-remote-evidence.md
artifacts/<slug>/04-root-cause.md
artifacts/<slug>/05-validation-or-repro-code.ext
artifacts/<slug>/06-backend-validation-guide.md
artifacts/<slug>/07-next-actions.md
```

Use subdirectories only for raw evidence or large generated material:

```text
artifacts/<slug>/runs/<run-id>/...
artifacts/<slug>/tests/...
artifacts/<slug>/export/...
```

If a case directory already exists, append new numbered files or revise existing root files; do not bury the final story in nested `reports/`, `problem/`, or `analysis/` directories.

A Makefile is optional. Use it when the case has repeatable commands worth exposing. If used, keep it at `artifacts/<slug>/Makefile` and make its targets append raw evidence under `runs/`.

## Investigation Workflow

1. Define the symptom and success criteria.
   Record the observed behavior, expected behavior, exact command, inputs, versions, commit hashes, and what would count as "root cause found" or "blocked by dependency".

2. Build a triggering use case.
   Keep the original repro under `tests/original/` and create minimized variants under `tests/minimized/`. Prefer executable tests that the Makefile can run. Preserve failing and passing variants when they clarify the boundary.

3. Capture every meaningful run.
   Use `make test TEST_CMD='...'` or `scripts/capture_run.py` so each run gets a stable `runs/<run-id>/` directory with command, logs, exit code, duration, environment, and artifacts.

4. Inspect the compiler pipeline.
   Choose debug methods based on the stack: Triton lowering/TTIR/TTGIR/LLVM IR/PTX, MLIR pass dumps and reproducers, LLVM `opt`/`llc`/`clang -cc1`, assembly, pass remarks, verifier output, crash stack, or bisect data.

5. Keep a written reasoning trail.
   Update the flat numbered root files. The order should show how the investigation progressed: problem → code path → remote/compiler evidence → root cause → validation/repro code → backend handoff questions → next actions. Include failed hypotheses and why they were ruled out.

6. Link evidence precisely.
   Reports must link to local logs/artifacts and repository source lines. Prefer commit-pinned remote links when a GitHub remote exists; otherwise use local relative links with `path:line` labels. Include line numbers for every code claim.

7. Decide outcome.
   End with one of: root cause found, strongly narrowed, upstream/dependency blocked, environment blocked, or unreproduced. For blockers, create an export bundle and include a handoff section with exact next questions.

## Remote Experiment Worktrees

Remote compiler validation may use dirty throwaway state, but it must not use
ad hoc or shared state. The evidence contract stays the same: every remote
build, test, or probe must be tied to `artifacts/<NNN-slug>/` and a
`runs/<run-id>/` record.

### Isolated Worktree Rule

For u22/Triton-style validation, do not occupy a shared worktree such as
`triton-dev` unless the user explicitly assigned it. Each agent/session should
create or reuse its own remote worktree derived from the current branch plus a
unique suffix, for example:

```text
<branch>_<case-or-agent-suffix>
```

Use a filesystem-safe path by replacing `/` with `-` or another safe separator.
Record the chosen branch, suffix, and remote path in `01-problem.md` or
`03-remote-evidence.md`. This protects concurrent agents from stashing,
cleaning, or overwriting each other's work.

### Remote Runner Bootstrap

For Triton/u22 validation, use the `$triton-remote-dev` skill's bundled remote
runner. That skill owns the personal u22 workflow, including installing
`assets/remote-runner/remote`, selecting an isolated worktree, syncing by
patch/file/git, configuring shared ccache, stashing dirty state, and capturing
run evidence.

Typical pattern after loading `$triton-remote-dev`:

```bash
SKILL_DIR=/Users/luca/.config/agents/skills/triton-remote-dev
test -f remote || cp "$SKILL_DIR/assets/remote-runner/remote" remote
scp -o BatchMode=yes -o ConnectTimeout=10 \
  "$SKILL_DIR/assets/remote-runner/remote" \
  u22:<remote-worktree-path>/remote

make -f remote case CASE=007-my-issue CASE_TITLE="..."
make -f remote sync SYNC=patch REMOTE_WORKTREE=<remote-worktree-path>
make -f remote test CASE=007-my-issue REMOTE_WORKTREE=<remote-worktree-path>
```

If a matching dedicated branch/worktree already exists for the task, use it and
do not create another one. If the remote layout is unclear, inspect narrowly and
record the selected path before running tests.

### Shared Remote ccache

Isolated worktrees should not mean cold rebuilds. When the repository provides a runner or `$triton-remote-dev` has installed one,
configure shared ccache before expensive build validation:

```bash
make -f remote ccache-setup
make -f remote ccache-status
```

The remote validation environment should export a shared `CCACHE_DIR` and set
`CCACHE_BASEDIR` to the selected remote worktree so different isolated worktrees
can reuse cached compiler results for matching relative source paths. Capture
ccache configuration and stats in the run evidence when possible.

### Avoid Pre-Validation CI Pushes

Do not push an unverified branch to `origin` just to move code to the remote
host when that push would trigger GitLab CI. For pre-CI remote validation, prefer
non-CI sync methods into the isolated worktree:

- `SYNC=patch` for tracked dirty edits without committing; note that untracked
  files are not included.
- `SYNC=file` or explicit `scp` for one-file experiments or temporary repro
  transfer.
- A local-only remote/bare repo on the validation host is acceptable if the repo
  already provides one, but do not invent a GitLab push as the transport.

Use `SYNC=git` / `git push origin` only when the user explicitly wants the branch
published, CI/MR validation, or a team-visible handoff.

### Remote Dirty Worktree Policy

A dedicated remote worktree may still be dirty from a previous probe. The default
behavior should keep work moving while preserving that state:

- Before sync, if the remote worktree is dirty, stash it first rather than
  blocking the experiment.
- After validation, clean up remote leftovers by stashing them unless the user
  explicitly chooses to keep the dirty state.
- Capture cleanup output as `cleanup.log` under the run directory.
- Never silently overwrite remote edits. Never auto-drop stashes.
- Never stash/drop/cleanup a shared or unknown worktree without first confirming
  it belongs to this task/session.

Stash messages must be searchable and concurrency-safe. Include the workflow tag,
sync mode, local branch/head, case id, file path when relevant, remote worktree
suffix/path, reason, and timestamp, for example:

```text
remote-dev sync=patch branch=<branch> head=<sha> case=007-x worktree=<path-or-suffix> file=foo.py reason=pre-sync ts=<UTC>
remote-dev sync=validate branch=<branch> head=<sha> case=007-x worktree=<path-or-suffix> reason=post-validation-cleanup ts=<UTC>
```

When neither the repo-local nor `$triton-remote-dev` runner can be used, follow the same behavior manually: create
or select the isolated worktree first, create or update the case directory,
capture the exact SSH/SCP/patch command and logs under `runs/`, stash dirty
remote state before sync when needed, and clean up the remote worktree after the
experiment.

## Directory Standard

Default structure:

```text
artifacts/<slug>/
├── 00-README.md
├── 01-problem.md
├── 02-code-path.md
├── 03-remote-evidence.md
├── 04-root-cause.md
├── 05-validation-or-repro-code.ext
├── 06-backend-validation-guide.md
├── 07-next-actions.md
├── runs/
│   └── <run-id>/
│       ├── cmd.sh
│       ├── stdout.log
│       ├── stderr.log
│       ├── metadata.json
│       ├── env.txt
│       └── artifacts/
├── tests/
│   ├── original/
│   ├── minimized/
│   └── expected/
└── export/
    └── <case-slug>.tar.gz
```

Reading order must be flat and obvious from filenames. Use these names unless a case needs a better sequence:

1. `00-README.md` — reading guide and one-line conclusion
2. `01-problem.md` — symptom, expected behavior, environment, success criteria
3. `02-code-path.md` — source links and inferred compiler/lowering path
4. `03-remote-evidence.md` — reproduced commands, logs, IR/assembly facts
5. `04-root-cause.md` — narrowed cause, ruled-out hypotheses, confidence
6. `05-validation-or-repro-code.ext` — minimal code or script for another engineer
7. `06-backend-validation-guide.md` — dependency-owner validation steps/questions
8. `07-next-actions.md` — recommended fixes, risks, open decisions

Do not flatten raw logs into prose. Keep raw evidence under `runs/` or `tests/`, then summarize and link from numbered root files.

If a readable artifact naturally belongs in a nested directory (for example, 100 generated tests under `tests/minimized/` or a backend handoff package under `export/`), keep it nested but add a numbered symlink at the artifact root so the user can still read everything in order:

```text
artifacts/<slug>/05-minimized-tests -> tests/minimized/README.md
artifacts/<slug>/06-backend-handoff -> export/handoff.md
```

The symlink target should be inside the same artifact directory. Do not create project-root symlinks unless the user explicitly asks.

## Report Rules

Prefer the flat numbered Markdown files over generated HTML. A separate `report.html` is optional and only needed when the user explicitly asks for an HTML artifact or the handoff audience benefits from it.

`00-README.md` should be concise for humans: reading order, one-line conclusion, and status.

The later numbered files should be complete enough for AI/context reuse: commands, failed hypotheses, debug methods, exact file paths, source links, remaining uncertainty, and `Skills used` when relevant.

If using the old bundled `scripts/build_report.py`, treat it only as a helper. Move or summarize generated content into the flat root files before finishing.

## Export Rules

When blocked by an upstream or dependency owner, run `make bundle`. The export bundle must include:

- manifest and problem statement
- minimized repro and original repro when shareable
- run logs and generated compiler artifacts
- reports
- source links or copied source snippets if the recipient cannot access the repo
- a checksum manifest

Before exporting, remove secrets, proprietary data that should not be shared, and oversized build products that are not needed to reproduce or understand the issue.

## References

- Read `references/debug-methods.md` when selecting Triton/LLVM/MLIR/Clang investigation commands.
- Read `references/report-contract.md` before writing or revising reports.
- Read `references/handoff.md` when the case is blocked and must be packaged for another team.
