---
name: task-dashboard
description: Create or update a self-contained HTML dashboard for an active engineering task, debugging investigation, CI rollout, incident, compiler/backend issue, or long-running implementation. Use when the user asks for a dashboard, task board, mission-control view, progress page, visual status artifact, or wants to see the problem, solution, todos, attempts, current work, blockers, evidence, and overall progress in one HTML file.
---

# Task Dashboard

## Purpose

Turn messy task state into a readable, visual, self-contained HTML dashboard. Default to a dark "Mission Control" style that makes the current truth, active blocker, and next action obvious in the first screen.

## Output Contract

Create or update one HTML file:

```text
artifacts/<case-slug>/dashboard.html
```

If the current task already has an artifact directory, reuse it. If not, create a concise slug under `artifacts/`. Keep the HTML self-contained: inline CSS, inline JavaScript only if needed, no CDN, no external assets unless the user explicitly asks.

## Dashboard Content Model

Always extract or write these sections:

- Current truth: 3-5 short facts visible in the first viewport.
- Problem: the real symptom and why it matters.
- Solution: what has changed or proposed fix.
- Attempts ledger: tried options, outcome, and why kept/rejected.
- Now trying: current investigation or implementation step.
- Todo: ordered next actions with priorities.
- Evidence: commands, run ids, logs, file paths, CI links, or artifact paths.
- Progress: one overall number plus more precise sub-progress when useful.
- Blockers/risks: what can still fail or needs an owner.

If a fact is unknown, write `TBD` or `unknown` explicitly. Do not fake confidence.

## Visual Rules

Use `assets/mission-control-template.html` as the default template. Adapt content aggressively, but preserve these UI priorities:

1. First screen must answer: "What is fixed, what is broken, what is next?"
2. Use a command-center layout: status header, truth strip, signal/path diagram, attempts ledger, now-trying panel, todo stack, parameter/result heatmap when applicable.
3. Use dense but organized engineering UI. Prefer bands, panels, dividers, tables, timelines, and heatmaps over decorative cards.
4. Use color semantically:
   - green: passed/done
   - amber: pending/in progress/risk
   - red: failed/blocker
   - cyan/blue: neutral signal/path/info
5. Keep text readable. No tiny labels, clipped text, negative letter spacing, or viewport-scaled font sizes.
6. Avoid generic SaaS fluff, marketing hero sections, decorative orbs, emoji, and cards inside cards.

## Workflow

1. Identify the artifact target.
   - Reuse an existing `artifacts/<case>/dashboard.html` if present.
   - Otherwise create `artifacts/<case-slug>/dashboard.html`.

2. Gather task state.
   - Read nearby numbered reports, logs, diffs, test outputs, CI status, and existing artifact files.
   - Prefer current evidence over memory.
   - If this is a compiler/debug task, preserve run ids and exact failing parameters.

3. Fill the content model.
   - Write the first viewport first.
   - Put the active blocker in the largest or most visible first-screen region.
   - Put "what changed" and "what remains" beside each other.

4. Render the dashboard.
   - Prefer `scripts/render_dashboard.py` when the content fits its JSON input model.
   - For custom layouts, copy `assets/mission-control-template.html` and edit the HTML directly.

5. Verify.
   - Check the file exists and contains the current blocker, progress, todos, and evidence paths.
   - If a browser is available and the user is looking at the file, tell them to refresh the same `file://` URL.

## Script Use

Use the script for fast dashboard creation from structured state:

```bash
python3 /Users/luca/.config/agents/skills/task-dashboard/scripts/render_dashboard.py \
  --input artifacts/<case>/dashboard.json \
  --output artifacts/<case>/dashboard.html
```

The JSON schema is documented in `references/dashboard-content-model.md`.

## Report Style

Be direct and status-oriented. The dashboard is not a slide deck. It should help the user decide what to do next within 5 seconds.
