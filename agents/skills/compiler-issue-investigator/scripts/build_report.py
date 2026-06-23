#!/usr/bin/env python3
import argparse
import html
import json
import re
from pathlib import Path


SECTION_FILES = [
    ("Problem", "problem/statement.md"),
    ("Timeline", "analysis/timeline.md"),
    ("Hypotheses", "analysis/hypotheses.md"),
    ("Debug Methods", "analysis/debug-methods.md"),
    ("Findings", "analysis/findings.md"),
    ("Code Links", "analysis/code-links.md"),
]


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.exists() else ""


def first_line(text: str) -> str:
    skipped = {"problem statement", "symptom", "todo"}
    for line in text.splitlines():
        stripped = line.strip("# ").strip()
        if stripped and stripped.lower() not in skipped:
            return stripped
    return "Compiler investigation report"


def run_summary(case_dir: Path) -> str:
    runs_dir = case_dir / "runs"
    if not runs_dir.exists():
        return "No captured runs yet.\n"
    rows = []
    for meta in sorted(runs_dir.glob("*/metadata.json")):
        data = json.loads(meta.read_text())
        rel = meta.parent.relative_to(case_dir)
        report_rel = Path("..") / rel
        rows.append(
            f"- `{data.get('run_id')}` exit `{data.get('exit_code')}` in `{data.get('duration_seconds')}s`: "
            f"[stdout]({report_rel}/stdout.log), [stderr]({report_rel}/stderr.log), [metadata]({report_rel}/metadata.json)"
        )
    return "\n".join(rows) + ("\n" if rows else "No captured command runs yet.\n")


def markdown_to_html(md: str) -> str:
    out = []
    in_list = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if line.startswith("### "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h3>{html.escape(line[4:])}</h3>")
        elif line.startswith("## "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h2>{html.escape(line[3:])}</h2>")
        elif line.startswith("# "):
            if in_list:
                out.append("</ul>")
                in_list = False
            out.append(f"<h1>{html.escape(line[2:])}</h1>")
        elif line.startswith("- "):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{linkify(html.escape(line[2:]))}</li>")
        elif not line:
            if in_list:
                out.append("</ul>")
                in_list = False
        else:
            out.append(f"<p>{linkify(html.escape(line))}</p>")
    if in_list:
        out.append("</ul>")
    return "\n".join(out)


def linkify(text: str) -> str:
    pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    return pattern.sub(lambda m: f'<a href="{html.escape(m.group(2), quote=True)}">{html.escape(m.group(1))}</a>', text)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Markdown and HTML reports for a compiler case.")
    parser.add_argument("--case-dir", required=True)
    args = parser.parse_args()
    case_dir = Path(args.case_dir).resolve()
    reports = case_dir / "reports"
    reports.mkdir(parents=True, exist_ok=True)

    manifest = read(case_dir / "manifest.yaml")
    problem = read(case_dir / "problem/statement.md")
    title = first_line(problem)

    parts = [
        f"# {title}",
        "",
        "## Executive Summary",
        "TODO: Summarize symptom, current status, strongest evidence, and next action.",
        "",
        "## Manifest",
        "```yaml",
        manifest.strip(),
        "```",
        "",
        "## Captured Runs",
        run_summary(case_dir),
    ]
    for heading, rel in SECTION_FILES:
        parts.extend([f"## {heading}", read(case_dir / rel).strip() or "TODO", ""])

    md = "\n".join(parts).strip() + "\n"
    (reports / "report.md").write_text(md)

    body = markdown_to_html(md)
    css = """
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;line-height:1.5;margin:0;color:#202124;background:#f7f7f4}
main{max-width:1040px;margin:0 auto;padding:40px 28px 72px;background:#fff;min-height:100vh}
h1{font-size:32px;margin:0 0 24px}h2{font-size:21px;margin-top:32px;border-top:1px solid #ddd;padding-top:18px}
h3{font-size:17px;margin-top:22px}p,li{font-size:14px}code,pre{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
pre{background:#f1f3f4;padding:12px;overflow:auto}a{color:#0b57d0;text-decoration:none}a:hover{text-decoration:underline}
"""
    html_doc = f"<!doctype html><html><head><meta charset='utf-8'><title>{html.escape(title)}</title><style>{css}</style></head><body><main>{body}</main></body></html>"
    (reports / "report.html").write_text(html_doc)
    print(reports / "report.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
