---
name: triton-remote-dev
description: Personal Triton remote-development workflow for Luca. Use when syncing local Triton changes to u22/182, creating isolated remote worktrees, installing the bundled remote runner, using patch/file/git sync without unintended GitLab CI pushes, preserving dirty remote state with stash/cleanup hygiene, configuring per-worktree venv and shared ccache, and running remote Nova build/test/dev-install through make -f remote. This is a personal workflow, not a team/shared process.
---

# Triton Personal Remote Development Workflow

Use this skill for Luca's personal Triton remote development loop. This workflow
is personal and should not be documented into the repository or shared as a team
convention unless the user explicitly asks.

## Environment

Local project root:

```text
/Users/luca/repos/triton
```

Remote host alias:

```text
u22
```

The user may call this the "182 server". In commands, use the SSH alias `u22`
unless the user provides a different host.

Remote master-only source repository:

```text
/root/repos/gpnpu/triton
```

Remote shared legacy worktree:

```text
/root/repos/gpnpu/triton-dev
```

Do not occupy `triton-dev` unless the user explicitly assigns it. Default to a
dedicated remote worktree per task/session.

Bundled remote runner:

```text
assets/remote-runner/remote
```

The runner is a makefile-like file named `remote`. It carries this workflow's
sync modes, artifact case creation, per-worktree venv, ccache environment, dirty-state stashing,
post-validation cleanup, and run evidence capture.

Important runner targets:

```bash
make -f remote case CASE=NNN-slug
make -f remote sync SYNC=patch REMOTE_WORKTREE=<remote-worktree-path>
make -f remote sync SYNC=file FILE=path/to/file REMOTE_WORKTREE=<remote-worktree-path>
make -f remote venv-setup REMOTE_WORKTREE=<remote-worktree-path>
make -f remote venv-status REMOTE_WORKTREE=<remote-worktree-path>
make -f remote ccache-setup
make -f remote ccache-status
make -f remote dev-install CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote build CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote test CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote test-nova-lit CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote test-nova-python CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote all CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
```

## Mandatory Rules

1. For u22 Triton build/test/dev-install, use the `remote` runner. If the repo
   lacks a local `remote` file, copy or invoke the bundled
   `assets/remote-runner/remote`.

2. When creating a new remote worktree, scp the same runner into that worktree:

   ```bash
   SKILL_DIR=/Users/luca/.config/agents/skills/triton-remote-dev
   scp -o BatchMode=yes -o ConnectTimeout=10 \
  "$SKILL_DIR/assets/remote-runner/remote" \
  u22:<remote-worktree-path>/remote
   ```

3. Use an isolated worktree by default. Derive its branch/path from the current
   branch plus a task/session suffix, replacing `/` with `-`.

4. Do not push an unverified branch to `origin` just to move code to u22 when
   that would trigger GitLab CI. Prefer `SYNC=patch` or `SYNC=file` for
   pre-CI validation. Use `SYNC=git` only when the user explicitly wants a
   branch published, CI/MR validation, or team-visible handoff.

5. Preserve dirty remote state. Before sync, stash dirty state instead of
   overwriting it. After validation, stash leftover experiment changes unless
   the user asks to keep them. Stash messages must be searchable and include
   workflow tag, sync mode, branch/head, case, worktree/path, reason, and UTC
   timestamp.

6. Every temporary test, build, or validation run must be tied to an
   `artifacts/<NNN-slug>/runs/<run-id>/` record. Use `CASE=NNN-slug` for runner
   validation targets.

7. Use a per-worktree venv. The runner defaults to
   `REMOTE_VENV=$(REMOTE_WORKTREE)/.venv-remote-dev`, exports
   `VIRTUAL_ENV`, prepends the venv `bin` directory to `PATH`, sets
   `PYTHONNOUSERSITE=1`, and passes `PYTHON=$(REMOTE_VENV)/bin/python` into
   remote make targets. Do not point multiple worktrees at the same venv unless
   the user explicitly asks.

8. Configure the venv and shared ccache before expensive validation:

   ```bash
   make -f remote venv-setup REMOTE_WORKTREE=<remote-worktree-path>
   make -f remote venv-status REMOTE_WORKTREE=<remote-worktree-path>
   make -f remote ccache-setup
   make -f remote ccache-status
   ```

## Standard Flow

### 1. Select or create the remote worktree

Use the master-only source repository as the clean base when creating a new
worktree:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 u22 'cd /root/repos/gpnpu/triton && \
  git worktree add -b <branch>_<suffix> <remote-worktree-path> <base-ref>'
```

If a matching dedicated worktree already exists for this task, reuse it. If the
layout is unclear, inspect narrowly and record the selected path before tests.

### 2. Install the runner locally and remotely

From `/Users/luca/repos/triton`:

```bash
SKILL_DIR=/Users/luca/.config/agents/skills/triton-remote-dev
test -f remote || cp "$SKILL_DIR/assets/remote-runner/remote" remote
scp -o BatchMode=yes -o ConnectTimeout=10 \
  "$SKILL_DIR/assets/remote-runner/remote" \
  u22:<remote-worktree-path>/remote
```

Prefer the repo-local `./remote` when it exists and has task-specific updates;
otherwise use the bundled asset with `make -f "$SKILL_DIR/assets/remote-runner/remote"`.

### 3. Create the local artifact case

```bash
make -f remote case CASE=NNN-slug CASE_TITLE="..."
```

### 4. Sync local changes

Default pre-CI sync:

```bash
make -f remote sync SYNC=patch REMOTE_WORKTREE=<remote-worktree-path>
```

For one-file or temporary repro transfer:

```bash
make -f remote sync SYNC=file FILE=path/to/file REMOTE_WORKTREE=<remote-worktree-path>
```

Only when the user explicitly wants the branch published or CI/MR-visible:

```bash
make -f remote sync SYNC=git REMOTE_WORKTREE=<remote-worktree-path>
```

### 5. Prepare venv and ccache

```bash
make -f remote venv-setup REMOTE_WORKTREE=<remote-worktree-path>
make -f remote venv-status REMOTE_WORKTREE=<remote-worktree-path>
make -f remote ccache-setup
make -f remote ccache-status
```

The venv must live under the selected remote worktree by default. The shared
resource is ccache, not Python packages or editable installs.

### 6. Validate

Run the narrowest meaningful target first:

```bash
make -f remote build CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote test-nova-lit CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
make -f remote test CASE=NNN-slug REMOTE_WORKTREE=<remote-worktree-path>
```

Use `make -f remote all CASE=NNN-slug ...` when the task needs the full default
remote validation surface.

## IFWA/VSI Toolkit Release Workflow

Remote IFWA/VSI toolkit release repository:

```text
/root/data/gpnpu/ifwa-toolkit-release
```

Mirror path that may contain the same release repository:

```text
/root/repos/gpnpu/ifwa-toolkit-release
```

Remote worktree toolkit symlink commonly used by Triton:

```text
<remote-worktree-path>/vsi
```

Do not assume `vsi` points at the intended toolkit version. Always verify:

```bash
ssh -o BatchMode=yes -o ConnectTimeout=10 u22 'cd "<remote-worktree-path>" && ls -l vsi && readlink -f vsi'
```

For one-off validation, avoid changing the `vsi` symlink. Source the desired
release directly inside the remote command and record it in the artifact run.
Only update `vsi` when the user explicitly wants that worktree default changed.

## Direct SSH Exceptions

Direct SSH/SCP is allowed for narrow inspection or setup that the runner does
not cover, such as listing worktrees, checking `vsi`, or creating the initial
remote worktree. It must not replace runner-based build/test/dev-install.

When using direct SSH for validation-like work, capture the command and output
under the active `artifacts/<NNN-slug>/runs/` directory or immediately summarize
it in `03-remote-evidence.md`.

## Cleanup

Do not run broad cleanup commands such as `git reset --hard` or `git clean -fd`
inside remote worktrees unless the user explicitly asks and understands the
effect. Use runner cleanup/stash behavior first:

```bash
make -f remote cleanup REMOTE_WORKTREE=<remote-worktree-path>
make -f remote stash-list REMOTE_WORKTREE=<remote-worktree-path>
```
