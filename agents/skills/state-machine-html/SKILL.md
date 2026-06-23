---
name: state-machine-html
description: Create editable, self-contained HTML dashboards for task state machines, progress flows, agent task monitors, workflow status pages, and review handoffs that need a clean top-down timeline rail, right-side state details, side exits, and local DasHTML-style save support.
---

# State Machine HTML

## Purpose

Create a concise local HTML dashboard that explains one concrete task as a state machine. Default to a top-down timeline rail with a sticky right-side detail panel. Avoid decorative arrows, graph clutter, and report-like sections.

## When To Use

Use this skill when the user asks for:

- A state-machine dashboard, task monitor, workflow status page, or progress map.
- An HTML artifact where clicking a state should reveal details.
- A template for agent task monitoring, build/review flow tracking, CI rollout state, incident state, or design iteration state.
- Editable local HTML that can save changes back to disk.

Do not use this for generic status reports that do not need state transitions.

## Output Contract

Create or update one self-contained HTML file:

```text
artifacts/<case-slug>/dashboard.html
```

Use the bundled renderer unless the task clearly needs custom layout:

```bash
python3 /Users/luca/.config/agents/skills/state-machine-html/scripts/render_state_machine_dashboard.py \
  --input artifacts/<case-slug>/state-machine.json \
  --output artifacts/<case-slug>/dashboard.html
```

For a quick starting point:

```bash
python3 /Users/luca/.config/agents/skills/state-machine-html/scripts/render_state_machine_dashboard.py \
  --write-example artifacts/<case-slug>/state-machine.json \
  --output artifacts/<case-slug>/dashboard.html
```

## Required Shape

The dashboard must keep this structure:

1. Top header: title, one-sentence purpose, real current state, save status.
2. Main left column: a single top-down timeline rail.
3. State cards: short label, one-line description, status tag.
4. Side exits: branch states shown inside the parent state card, not floating between cards.
5. Right rail: selected state detail with why, evidence, and exit condition.
6. Recent events: short timestamped list in the right rail.

## Visual Rules

- Prefer a timeline rail over arrows. Do not draw per-card arrow connectors.
- Use one continuous vertical rail to express flow direction.
- Keep side exits inside the state they branch from; use a small `↳` marker instead of connector lines.
- Current state must be visually obvious within five seconds.
- Right detail rail is non-optional; clicking any state updates it.
- Do not add buttons for normal state inspection.
- Avoid decorative-only graphics, graph-node spaghetti, gradient blobs, or oversized hero sections.
- Keep the page compact enough for the first viewport to show the current state and at least the next state.

## Editable Save Mode

Default generated pages are editable:

- Store the absolute output path in `data-dashtml-path`.
- Default all editable text to `contenteditable="false"`.
- Enter edit mode by double-clicking editable text.
- Save a browser draft to `localStorage` while typing.
- On blur, POST `{ "path": "<absolute-html-path>", "html": "<full document html>" }` to `http://127.0.0.1:8765/save`.
- Keep the right rail save status visible.
- Serialize a clean document: no runtime-only selected state, all `contenteditable` reset to `false`, state details persisted in `script#state-data`.

If overwrite save is needed, reuse an existing DasHTML save server on port `8765` when available. Otherwise start:

```bash
tmux new-session -d -s dashtml-dashboard-save 'cd <repo-or-root> && python3 /Users/luca/.config/agents/skills/dashtml/scripts/dashtml_save_server.py --root <repo-or-root> --port 8765'
```

## Configuration Schema

The renderer expects JSON:

```json
{
  "title": "Dashboard title",
  "subtitle": "One sentence explaining the task.",
  "current": "embed",
  "outputPath": "/absolute/path/to/dashboard.html",
  "states": [
    {
      "id": "request",
      "index": "01",
      "title": "收到请求",
      "summary": "做一个 agent task dashboard",
      "status": "done",
      "detail": {
        "kicker": "State 01",
        "body": "What this state means.",
        "why": "Why this state exists.",
        "evidence": "What proves this state.",
        "exit": "What moves the task onward."
      }
    }
  ],
  "sideExits": [
    {
      "parent": "embed",
      "id": "blocked",
      "title": "卡住",
      "summary": "需求不清或审美方向不稳",
      "kind": "wait",
      "detail": { "kicker": "Side Exit", "body": "...", "why": "...", "evidence": "...", "exit": "..." }
    }
  ],
  "recent": [
    { "time": "15:42", "text": "branch.display_reworked" }
  ]
}
```

Keep state IDs stable. Detail edits are persisted into `script#state-data`, so re-rendering from stale JSON can overwrite manual browser edits.

## Validation

Before finishing:

- Confirm no `<button>` elements are used for state inspection.
- Confirm the page has `data-dashtml-path`, `script#state-data`, `.flow`, `.detail-panel`, and `.side-exits` when side exits exist.
- Check JavaScript syntax, excluding `type="application/json"` scripts.
- Render desktop and narrow viewports; verify no horizontal overflow.
- Click at least one main state and one side exit; confirm the right detail rail changes and current state does not change.
- If editing is enabled, verify save server health or say save is browser-draft only.
