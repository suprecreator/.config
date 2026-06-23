# Dashboard Content Model

Use this reference when creating a structured input for `scripts/render_dashboard.py`.

## Minimal JSON

```json
{
  "title": "IFWA 0610 Mission Control",
  "subtitle": "Current task dashboard",
  "updated": "2026-06-15",
  "progress": 74,
  "chips": [
    {"label": "mxy/update", "tone": "info"},
    {"label": "sqrt/rsqrt fixed", "tone": "good"},
    {"label": "LayerNorm abort", "tone": "bad"}
  ],
  "truths": [
    {"label": "validated", "value": "16 / 16 pass", "detail": "sqrt and rsqrt pass", "tone": "good"},
    {"label": "active blocker", "value": "exit 134", "detail": "LayerNorm block2048 fp16 abort", "tone": "bad"}
  ],
  "problems": [
    {"label": "symptom", "tone": "bad", "text": "What fails and why it matters."}
  ],
  "solutions": [
    {"label": "keep", "tone": "good", "text": "What the fix does."}
  ],
  "attempts": [
    {"number": "01", "label": "failed", "tone": "bad", "text": "Tried option and outcome."}
  ],
  "now": [
    {"status": "!", "tone": "warn", "text": "Current active work.", "priority": "P0"}
  ],
  "todos": [
    {"status": "done", "tone": "good", "text": "Completed item.", "priority": "done"},
    {"status": "!", "tone": "warn", "text": "Next item.", "priority": "next"}
  ],
  "heatmap": {
    "columns": ["case", "dtype", "result", "evidence"],
    "rows": [
      {"cells": ["block2048", "fp16", "abort", "exit 134"], "tone": "bad"}
    ]
  },
  "evidence": [
    {"label": "runs", "tone": "info", "text": "artifacts/011-case/runs/101"}
  ]
}
```

## Tone Values

Use only:

- `good`
- `warn`
- `bad`
- `info`
- `note`

## Required First-Screen Facts

The first screen should include:

- strongest pass/fail validation fact
- active blocker
- current code/solution state
- release or CI state

## Progress Guidance

Use an honest progress estimate. Prefer sub-progress in text when one number is too coarse:

- implementation
- validation
- investigation
- CI/release
