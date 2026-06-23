#!/usr/bin/env python3
"""Render a self-contained Mission Control task dashboard from JSON."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "assets" / "mission-control-template.html"


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def tone(value: Any, default: str = "info") -> str:
    value = str(value or default)
    return value if value in {"good", "warn", "bad", "info", "note"} else default


def status_class(value: Any) -> str:
    value = str(value or "").lower()
    if value in {"done", "pass", "passed", "ok", "✓"}:
        return "done"
    if value in {"block", "blocked", "fail", "failed", "x", "×"}:
        return "block"
    return "now"


def status_text(value: Any) -> str:
    value = str(value or "!")
    if value.lower() in {"done", "pass", "passed", "ok"}:
        return "✓"
    if value.lower() in {"block", "blocked", "fail", "failed"}:
        return "×"
    return value[:2]


def render_chips(items: list[dict[str, Any]]) -> str:
    return "\n".join(f'<span class="chip {tone(item.get("tone"))}">{esc(item.get("label", ""))}</span>' for item in items)


def render_truths(items: list[dict[str, Any]]) -> str:
    cards = []
    for item in items[:4]:
        cards.append(f"""
      <article class="truth {tone(item.get("tone"))}">
        <small>{esc(item.get("label", ""))}</small>
        <strong>{esc(item.get("value", ""))}</strong>
        <p>{esc(item.get("detail", ""))}</p>
      </article>""")
    return "\n".join(cards)


def render_rows(items: list[dict[str, Any]]) -> str:
    rows = []
    for item in items:
        rows.append(f"""
          <div class="row">
            <span class="tag {tone(item.get("tone"))}">{esc(item.get("label", ""))}</span>
            <p class="desc">{esc(item.get("text", ""))}</p>
          </div>""")
    return "\n".join(rows)


def render_attempts(items: list[dict[str, Any]]) -> str:
    attempts = []
    for item in items[:5]:
        attempts.append(f"""
          <div class="attempt">
            <span class="num">{esc(item.get("number", ""))}</span>
            <span class="tag {tone(item.get("tone"))}">{esc(item.get("label", ""))}</span>
            <p class="desc">{esc(item.get("text", ""))}</p>
          </div>""")
    return "\n".join(attempts)


def render_todo(items: list[dict[str, Any]]) -> str:
    todos = []
    for item in items:
        status = item.get("status", "!")
        todos.append(f"""
          <div class="todo-item">
            <span class="check {status_class(status)}">{esc(status_text(status))}</span>
            <p class="desc">{esc(item.get("text", ""))}</p>
            <span class="priority">{esc(item.get("priority", ""))}</span>
          </div>""")
    return "\n".join(todos)


def render_heatmap(model: dict[str, Any] | None) -> str:
    if not model:
        return ""
    columns = model.get("columns") or []
    rows = model.get("rows") or []
    if not columns:
        return ""
    cells = [f'<div class="head">{esc(col)}</div>' for col in columns]
    for row in rows:
        row_tone = tone(row.get("tone"), "info")
        cell_class = {"good": "pass", "bad": "fail", "warn": "pending"}.get(row_tone, "")
        for cell in row.get("cells", []):
            cells.append(f'<div class="{cell_class}">{esc(cell)}</div>')
    return f"""
      <article class="panel">
        <h2>{esc(model.get("title", "Parameter Heatmap"))}</h2>
        <div class="heatmap" style="--heatmap-cols: {len(columns)}" role="table">
          {''.join(cells)}
        </div>
      </article>"""


def render_signal_path(data: dict[str, Any]) -> str:
    nodes = data.get("signal_nodes") or [
        {"title": "problem", "detail": "current task", "tone": "warn"},
        {"title": "solution", "detail": "active fix", "tone": "good"},
        {"title": "blocker", "detail": "next risk", "tone": "bad"},
    ]
    labels = (nodes + [{}] * 3)[:3]
    return f"""
        <div class="signal-map">
          <svg viewBox="0 0 650 260" role="img" aria-label="Task signal path">
            <defs>
              <marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
                <path d="M 0 0 L 10 5 L 0 10 z" fill="#35d5ff"></path>
              </marker>
            </defs>
            <g class="node {tone(labels[0].get("tone"))}">
              <rect x="26" y="92" width="170" height="72"></rect>
              <text x="111" y="123" text-anchor="middle">{esc(labels[0].get("title", ""))}</text>
              <text class="sub" x="111" y="145" text-anchor="middle">{esc(labels[0].get("detail", ""))}</text>
            </g>
            <path class="wire" d="M 202 128 C 255 128, 278 128, 326 128"></path>
            <g class="node {tone(labels[1].get("tone"))}">
              <rect x="332" y="92" width="170" height="72"></rect>
              <text x="417" y="123" text-anchor="middle">{esc(labels[1].get("title", ""))}</text>
              <text class="sub" x="417" y="145" text-anchor="middle">{esc(labels[1].get("detail", ""))}</text>
            </g>
            <path class="wire bad" d="M 418 168 C 418 206, 504 212, 536 178"></path>
            <g class="node {tone(labels[2].get("tone"))}">
              <rect x="456" y="28" width="170" height="72"></rect>
              <text x="541" y="59" text-anchor="middle">{esc(labels[2].get("title", ""))}</text>
              <text class="sub" x="541" y="81" text-anchor="middle">{esc(labels[2].get("detail", ""))}</text>
            </g>
          </svg>
        </div>"""


def render_body(data: dict[str, Any]) -> str:
    progress = max(0, min(100, int(data.get("progress", 0))))
    progress_lines = data.get("progress_lines") or []
    progress_html = "\n".join(f"<p>{esc(line)}</p>" for line in progress_lines)
    evidence = data.get("evidence") or []
    heatmap_html = render_heatmap(data.get("heatmap"))
    evidence_html = render_rows(evidence)

    return f"""
  <main>
    <section class="mission-header" aria-label="Mission control header">
      <header class="hero">
        <div>
          <div class="eyebrow">{render_chips(data.get("chips") or [])}</div>
          <h1>{esc(data.get("title", "Task Mission Control"))}</h1>
          <p class="hero-subtitle">{esc(data.get("subtitle", ""))}</p>
        </div>
        <p class="mono">{esc(data.get("current_truth", ""))}</p>
      </header>
      <aside class="progress-tower" aria-label="Overall progress">
        <div class="ring" style="--progress: {progress}">
          <div>
            <strong>{progress}%</strong>
            <span>overall</span>
          </div>
        </div>
        <div class="tower-lines">{progress_html}</div>
      </aside>
    </section>

    <section class="truth-strip" aria-label="Current truth">{render_truths(data.get("truths") or [])}</section>

    <section class="grid-main">
      <article class="panel">
        <h2>Problem</h2>
        <div class="stack">{render_rows(data.get("problems") or [])}</div>
      </article>
      <article class="panel">
        <h2>Signal Path</h2>
        {render_signal_path(data)}
      </article>
      <aside class="panel">
        <h2>Solution</h2>
        <div class="stack">{render_rows(data.get("solutions") or [])}</div>
      </aside>
    </section>

    <section class="split">
      <article class="panel">
        <h2>Attempts Ledger</h2>
        <div class="attempts">{render_attempts(data.get("attempts") or [])}</div>
      </article>
      <aside class="panel dim">
        <h2>Now Trying</h2>
        <div class="todo">{render_todo(data.get("now") or [])}</div>
      </aside>
    </section>

    <section class="split">
      {heatmap_html}
      <aside class="panel">
        <h2>Todo</h2>
        <div class="todo">{render_todo(data.get("todos") or [])}</div>
      </aside>
    </section>

    <section class="panel">
      <h2>Files And Evidence</h2>
      <div class="stack">{evidence_html}</div>
      <p class="footer">Updated {esc(data.get("updated", ""))} · Mission Control layout · self-contained HTML</p>
    </section>
  </main>"""


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Dashboard JSON path, or '-' for stdin")
    parser.add_argument("--output", required=True, help="Output HTML path")
    args = parser.parse_args()

    if args.input == "-":
        import sys
        data = json.load(sys.stdin)
    else:
        data = json.loads(Path(args.input).read_text(encoding="utf-8"))

    template = TEMPLATE.read_text(encoding="utf-8")
    body = render_body(data)
    html_text = template.replace("{{TITLE}}", esc(data.get("title", "Task Dashboard"))).replace("{{BODY}}", body)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(html_text, encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
