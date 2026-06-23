---
name: dashtml
description: Create concise, editable, self-contained HTML dashboards for complex engineering work, investigations, merge requests, CI status, implementation summaries, technical plans, tradeoff reviews, and project handoffs. Use when the user asks for an HTML dashboard, visual summary, project dashboard, MR dashboard, status page, investigation artifact, or wants "目标 / 方案 / 改动 / tradeoff / CI / 下一步" presented as a scannable local HTML file.
---

# DasHTML

## Purpose

Produce a local HTML dashboard that turns messy engineering context into a clear status artifact. Optimize for fast scanning, decision making, editing, and handoff.

## Default Output

Create one `.html` file near the relevant artifacts or docs. Prefer:

- Existing artifact directory if one exists, such as `artifacts/<case>/`.
- Otherwise a clearly named file under the current repo, such as `artifacts/<topic>-dashboard.html`.
- Inline CSS and JavaScript for dashboard code. Do not use remote CDNs at runtime.
- If a library is needed, vendor it next to the artifact, for example `vendor/fabric.min.js`, and reference it relatively.
- Main content should be editable without visible controls: default to read mode, enter edit mode on double-click, and save when focus leaves the editable body. Keep the right-side key-info rail non-editable.
- When freeform notes or drawings are requested, keep section content full-width and add an annotation dock at the end of each major section instead of making the whole section a left/right split.

## Templates

Start from a bundled template instead of rewriting the page skeleton:

- `templates/dashboard-basic.html`: three-column dashboard with TOC, editable body, right rail, responsive layout, and local save integration.
- `templates/dashboard-whiteboard.html`: basic dashboard plus Fabric.js whiteboards at each major section.

Template workflow:

1. Copy the selected template next to the target artifact.
2. Replace placeholders such as `__ABS_HTML_PATH__`, `__DASHBOARD_TITLE__`, `__SECTION_1_TITLE__`, and link/status placeholders.
3. For the whiteboard template, vendor Fabric next to the artifact as `vendor/fabric.min.js`.
4. Keep template structure intact unless the task clearly needs a different layout.

## Editable Save Mode

Static HTML cannot silently overwrite itself. For dashboards that should edit in place, use the local save server:

```bash
python3 /Users/luca/.config/agents/skills/dashtml/scripts/dashtml_save_server.py --root <repo-or-artifact-root> --port 8765
```

Recommended long-running form:

```bash
tmux new-session -d -s dashtml 'cd <repo> && python3 /Users/luca/.config/agents/skills/dashtml/scripts/dashtml_save_server.py --root <repo> --port 8765'
```

Generated editable HTML should:

- Store the absolute target path in `data-dashtml-path`.
- Default the main content to `contenteditable="false"`.
- Enter edit mode on double-click by setting `contenteditable="true"` and focusing the body.
- Save a browser draft to `localStorage` while typing.
- On focus leaving the editable body, POST `{ "path": "<absolute-html-path>", "html": "<full document html>" }` to `http://127.0.0.1:8765/save`, then return to read mode.
- Avoid visible edit/export/reset buttons unless the user explicitly asks for them.
- Show save status clearly: browser draft saved, file saved, or save server unavailable.
- When saving generated HTML, serialize a clean clone of the document. Strip runtime-only DOM created by libraries, reset `contenteditable` to `false`, and keep persistent state in JSON script tags or normal HTML, not in generated wrapper DOM.

## Required Structure

Use three visible sections by default:

1. **Top: Goal and Important Info**
   - What we are trying to do.
   - Current scope and non-scope.
   - Proposed solution in one paragraph.
   - Important links: MR/PR, CI, commits, docs, artifacts.
   - Current status and freshness. If live status cannot be verified, say so explicitly.

2. **Middle: Changes and Tradeoffs**
   - Main code or project changes.
   - Why each change exists.
   - Tradeoffs and rejected alternatives.
   - Risk notes, constraints, and ownership boundaries.

3. **Bottom: Useful Details**
   - Test matrix or validation evidence.
   - Commands that matter.
   - Key files.
   - Known blockers.
   - Next steps.

Do not add a generic "lessons learned" section unless the user asks for one.

## Layout

Default to a Codex-like dark engineering UI:

- Left navigation column: sticky section table of contents when there is room; collapse it to a top horizontal nav when the viewport is narrow.
- Main column: editable content sections and lists.
- Right sticky rail: key links, environment, progress, status, freshness, and save state.
- Restrained dark palette, compact spacing, scan-friendly tables, badges, and code pills.
- No decorative-only visuals.

Section and annotation layout rules:

- Keep each major section's primary content full-width. Do not split tables, cards, timelines, or flow content into a narrow left column with annotation content on the right; it causes clipping and cramped layouts.
- Put editable notes and whiteboards in a bottom `annotation-dock` after the section content. The dock should be a two-column grid only for annotation tools: left `textarea.notes-panel`, right `.whiteboard`.
- Collapse `annotation-dock` to one column at tablet/mobile widths. Keep the main section content unchanged above it.
- Use `textarea` for freeform user notes, not nested `contenteditable` panels. Nested editable regions inside an editable article cause browser DOM duplication when pressing Enter.
- Set `contenteditable="false"` on annotation docks and whiteboards. Let the `textarea` own text editing.
- Before serializing or autosaving, sync every `textarea.notes-panel` value into `defaultValue`/`textContent`, so edited notes survive a full HTML save and reload.
- After structural HTML changes, bump the `editableDoc` localStorage key version, but keep the whiteboard storage key stable unless intentionally resetting drawings.

Responsive rules:

- Do not let the page create horizontal overflow. Verify `document.documentElement.scrollWidth <= innerWidth + 2`.
- Use `min-width: 0` on grid children and content columns.
- Let cards/flow blocks use `auto-fit` grids instead of fixed 3/4-column layouts at narrow widths.
- Let long `code` and monospace labels wrap with `overflow-wrap: anywhere`.
- Put wide tables inside a scroll wrapper such as `.table-scroll`.
- Three-column app layouts should degrade early enough for the actual viewport. If unsure, collapse side navigation before the page clips content.

Editing UI rules:

- Do not draw heavy or full-section borders while the document is in edit mode. Prefer caret color and the status rail for feedback.
- Keep visible controls sparse. Do not add edit/save/export buttons by default.
- Avoid visible edit borders around full sections. Use subtle focus state only on actual inputs such as `textarea.notes-panel`.

## Whiteboard Blocks

When the user wants inline annotations or drawing, add Fabric.js whiteboard blocks:

- Vendor Fabric locally, for example `artifacts/<case>/vendor/fabric.min.js`; do not rely on CDN at runtime.
- Add a whiteboard inside the section's bottom `annotation-dock` when annotation space is requested; do not put the whiteboard in a narrow side column beside the section's main content.
- Pair each whiteboard with a same-height-or-resizable `textarea.notes-panel` for typed notes.
- Default tools: `Select`, `Pen`, `Text`, `Rect`, `Del`, `Clear`.
- Use real `<button type="button">` controls for tools, not clickable `<span>` elements.
- Put the whiteboard title and tool buttons on separate rows, align buttons left, and allow wrapping. Avoid a single cramped header row.
- Support deleting selected objects with both the `Del` tool and `Delete` / `Backspace`.
- Use Fabric 7-compatible APIs: `canvas.setDimensions(...)` and `canvas.getScenePoint(event)`; do not use older-only `setWidth`, `setHeight`, or `getPointer` without a compatibility fallback.
- Keep Fabric object data in `<script id="whiteboardData" type="application/json">...</script>`.
- Before saving the full document, clean whiteboard runtime DOM back to plain `<canvas class="board-canvas">` and regenerate the tool buttons. This prevents Fabric wrapper DOM or stale tool markup from being persisted.
- Stop whiteboard click/double-click events from bubbling into body edit mode.
- Ignore `.annotation-dock` in double-click-to-edit handlers so clicking or selecting notes does not toggle article editing.

## Workflow

1. Gather facts from local files first:
   - Read existing summaries, artifacts, diffs, logs, and test files.
   - For MR/CI dashboards, query the relevant CLI/API if available.
   - If a live service times out, use the last known state and label it as stale or unverified.

2. Decide the dashboard contract:
   - Audience: reviewer, teammate, future self, or decision maker.
   - Main question: status, plan, review, diagnosis, or handoff.
   - Evidence level: exact commands/results when available; otherwise clearly marked assumptions.

3. Build the HTML:
   - Use semantic HTML.
   - Use restrained engineering-dashboard styling.
   - Use cards, tables, timelines, flow diagrams, and badges only when they clarify information.
   - Keep text short. Prefer dense, scan-friendly labels over long prose.
   - Avoid decorative-only visuals.
   - If whiteboards are present, keep user drawings in JSON and keep the rendered canvas disposable.

4. Validate:
   - Run a lightweight structure check, for example search for the three main section titles and key links.
   - Check that annotation dashboards have one `annotation-dock`, one `textarea.notes-panel`, and one `.whiteboard` per annotated major section; reject stale `section-grid` / `section-side` annotation layouts.
   - Check inline JavaScript syntax. Exclude `type="application/json"` script tags from JS syntax checks.
   - Check HTML tag balance after excluding scripts.
   - For responsive dashboards, validate at a narrow width and a desktop width; check for horizontal overflow.
   - For notes, verify pressing Enter in the notes area creates a new line in the same textarea, not new text panels.
   - For whiteboards, verify tool switching, object creation, object deletion, and save status on a temporary copy when possible so real annotations are not polluted.
   - Run formatter/pre-commit if appropriate for the repo.
   - If editable save is enabled, start or verify the local save server and report how to restart it.
   - Report the absolute file path.

## Style Rules

- Write in the user's language.
- Keep the first viewport useful: goal, status, links, and primary risk should be visible early.
- Make status labels precise: `pass`, `running`, `blocked`, `unknown`, `stale`, `needs refresh`.
- For CI or remote state, include timestamp or freshness note.
- Do not over-explain basic HTML/CSS choices in the final answer.
- Do not claim a test or CI passed unless it was verified or backed by an artifact.

## Good Dashboard Blocks

Use these blocks when helpful:

- Support matrix: capability vs compile/lit/runtime.
- Pipeline map: Python -> IR -> lowering -> runtime.
- Change list: file/module, change, reason, status.
- Tradeoff cards: option, why chosen, cost.
- Evidence panel: command, result, artifact/log path.
- Next-plan checklist: concrete follow-up work.
- Annotation dock: full-width section content followed by `textarea` notes plus Fabric canvas.
- Section whiteboard: Fabric canvas for freehand notes, text, boxes, and deletions.

## Final Response

Keep the final response short:

- Link the HTML file with an absolute local path.
- Mention whether editable overwrite save is backed by the local server.
- Mention validation done.
- Mention any stale/unverified live data.
