#!/usr/bin/env python3
"""Render an editable state-machine HTML dashboard from JSON config."""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any


SKILL_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_PATH = SKILL_DIR / "assets" / "state-machine-dashboard-template.html"


EXAMPLE_CONFIG: dict[str, Any] = {
    "title": "Dashboard 设计任务",
    "subtitle": "用这张图监控一个具体任务的状态、分支和下一步。",
    "current": "embed",
    "states": [
        {
            "id": "request",
            "index": "01",
            "title": "收到请求",
            "summary": "做一个 agent task dashboard",
            "status": "done",
            "detail": {
                "kicker": "State 01",
                "body": "用户要一个用于监控 agent task 的 state machine dashboard。",
                "why": "这是任务入口，决定页面应该是可用 dashboard，而不是说明文字。",
                "evidence": "目标、产物路径和浏览器打开方式都已经确定。",
                "exit": "第一版页面可见，能开始根据反馈调整。",
            },
        },
        {
            "id": "simplify",
            "index": "02",
            "title": "删繁就简",
            "summary": "去掉报告感，只保留状态",
            "status": "done",
            "detail": {
                "kicker": "State 02",
                "body": "删除无关 sections，让当前状态成为第一视觉重点。",
                "why": "dashboard 的价值是快速判断状态；内容越多，状态越不明显。",
                "evidence": "页面只保留状态流、右侧详情和最近事件。",
                "exit": "主状态和下一步可以在五秒内看懂。",
            },
        },
        {
            "id": "draw",
            "index": "03",
            "title": "重画流程",
            "summary": "从箭头图改为 timeline rail",
            "status": "done",
            "detail": {
                "kicker": "State 03",
                "body": "使用连续轨道表达流转，不再画卡片之间的箭头。",
                "why": "箭头容易变丑、抢戏、产生错位；timeline rail 更稳。",
                "evidence": "左侧 rail 贯穿主流程，卡片只负责承载状态内容。",
                "exit": "轨道清楚，分支不悬空。",
            },
        },
        {
            "id": "embed",
            "index": "04",
            "title": "嵌入任务",
            "summary": "让 dashboard 监控自己的设计过程",
            "status": "now",
            "detail": {
                "kicker": "State 04",
                "body": "这张 dashboard 正在描述它自己的设计任务。",
                "why": "具体任务比抽象流程更容易判断当前进展。",
                "evidence": "标题、状态名、右侧详情和 recent events 都指向当前任务。",
                "exit": "点击状态可切详情，当前状态不随查看项变化。",
            },
        },
        {
            "id": "verify",
            "index": "05",
            "title": "验证体验",
            "summary": "检查交互、布局和保存",
            "status": "next",
            "detail": {
                "kicker": "State 05",
                "body": "在真实浏览器里检查点击、编辑保存和响应式布局。",
                "why": "HTML dashboard 必须在实际 file:// 页面成立。",
                "evidence": "无横向溢出，点击状态能更新右侧详情。",
                "exit": "所有状态都有可用详情，保存服务可用或明确降级。",
            },
        },
        {
            "id": "done",
            "index": "06",
            "title": "交付",
            "summary": "一屏看懂，点状态看细节",
            "status": "ready",
            "detail": {
                "kicker": "State 06",
                "body": "页面可以作为任务状态监控视图使用。",
                "why": "它保留了状态、分支、详情和可编辑保存。",
                "evidence": "产物是一个自包含 HTML 文件。",
                "exit": "终态，除非继续收到设计反馈。",
            },
        },
    ],
    "sideExits": [
        {
            "parent": "embed",
            "id": "blocked",
            "title": "卡住",
            "summary": "需求不清或方向不稳",
            "kind": "wait",
            "detail": {
                "kicker": "Side Exit",
                "body": "目标表达、审美方向或交互预期不明确时进入这里。",
                "why": "设计类任务最容易卡在“看起来不对，但说不清哪里不对”。",
                "evidence": "需要更明确的判断标准或新反馈。",
                "exit": "拿到明确方向后回到当前主状态。",
            },
        },
        {
            "parent": "embed",
            "id": "failed",
            "title": "失败",
            "summary": "页面仍然丑或看不懂",
            "kind": "fail",
            "detail": {
                "kicker": "Side Exit",
                "body": "如果页面只是炫技，或者状态和详情关系不清楚，就进入失败。",
                "why": "监控面板必须先清楚，再谈好看。",
                "evidence": "失败信号包括箭头喧宾夺主、分支悬空、交互入口分散。",
                "exit": "回到删繁就简，减少元素，再重画。",
            },
        },
    ],
    "recent": [
        {"time": "15:42", "text": "branch.display_reworked"},
        {"time": "15:25", "text": "editable.save_enabled"},
        {"time": "15:10", "text": "timeline.rail_selected"},
    ],
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def status_class(status: str) -> str:
    if status == "done":
        return "done"
    if status in {"now", "current", "running"}:
        return "current"
    return ""


def normalize_config(config: dict[str, Any], output: Path) -> dict[str, Any]:
    config = dict(config)
    config.setdefault("title", "State Machine Dashboard")
    config.setdefault("subtitle", "A concrete task state-machine dashboard.")
    config.setdefault("states", [])
    config.setdefault("sideExits", [])
    config.setdefault("recent", [])
    if not config["states"]:
        raise ValueError("config.states must contain at least one state")
    config.setdefault("current", config["states"][0]["id"])
    config["outputPath"] = str(output.resolve())
    return config


def state_detail(state: dict[str, Any]) -> dict[str, str]:
    detail = dict(state.get("detail", {}))
    return {
        "kicker": str(detail.get("kicker", state.get("index", state["id"]))),
        "title": str(detail.get("title", state.get("title", state["id"]))),
        "body": str(detail.get("body", "")),
        "why": str(detail.get("why", "")),
        "evidence": str(detail.get("evidence", "")),
        "exit": str(detail.get("exit", "")),
    }


def build_state_data(config: dict[str, Any]) -> dict[str, dict[str, str]]:
    data: dict[str, dict[str, str]] = {}
    for state in config["states"]:
        data[state["id"]] = state_detail(state)
        data[state["id"]]["title"] = str(state.get("title", data[state["id"]]["title"]))
    for side_exit in config.get("sideExits", []):
        data[side_exit["id"]] = state_detail(side_exit)
        data[side_exit["id"]]["title"] = str(side_exit.get("title", data[side_exit["id"]]["title"]))
    return data


def build_side_exits(parent: str, exits: list[dict[str, Any]]) -> str:
    matches = [item for item in exits if item.get("parent") == parent]
    if not matches:
        return ""
    items = ['            <div class="side-exits" aria-label="side exits from this state">', '              <div class="exit-label">Side exits from this state</div>']
    for item in matches:
        kind = item.get("kind", "wait")
        classes = "branch " + ("fail" if kind == "fail" else "wait")
        items.append(
            f'''              <div class="{classes}" data-state="{esc(item["id"])}" role="button" tabindex="0">
                <strong data-editable contenteditable="false">{esc(item.get("title", item["id"]))}</strong>
                <span data-editable contenteditable="false">{esc(item.get("summary", ""))}</span>
              </div>'''
        )
    items.append("            </div>")
    return "\n".join(items)


def build_flow(config: dict[str, Any]) -> str:
    current = config["current"]
    side_exits = config.get("sideExits", [])
    chunks: list[str] = []
    for state in config["states"]:
        classes = ["flow-step"]
        cls = status_class(state.get("status", ""))
        if cls:
            classes.append(cls)
        if state["id"] == current:
            classes.extend(["selected", "has-exits"])
        side_html = build_side_exits(state["id"], side_exits)
        if side_html and "has-exits" not in classes:
            classes.append("has-exits")
        chunks.append(
            f'''          <div class="{' '.join(classes)}" data-state="{esc(state["id"])}" role="button" tabindex="0">
            <div class="index">{esc(state.get("index", ""))}</div>
            <div class="flow-copy">
              <strong data-editable contenteditable="false">{esc(state.get("title", state["id"]))}</strong>
              <span data-editable contenteditable="false">{esc(state.get("summary", ""))}</span>
            </div>
            <span class="state-tag">{esc(state.get("status", ""))}</span>
{side_html}
          </div>'''
        )
    return "\n\n".join(chunks)


def build_recent(config: dict[str, Any]) -> str:
    rows = []
    for item in config.get("recent", []):
        rows.append(
            f'''          <div class="recent-row"><span class="time">{esc(item.get("time", ""))}</span><span data-editable contenteditable="false">{esc(item.get("text", ""))}</span></div>'''
        )
    return "\n".join(rows) or '          <div class="recent-row"><span class="time">--:--</span><span data-editable contenteditable="false">unknown</span></div>'


def progress_stops(config: dict[str, Any]) -> tuple[str, str]:
    states = config["states"]
    current_index = next((i for i, state in enumerate(states) if state["id"] == config["current"]), 0)
    total = max(len(states) - 1, 1)
    done_stop = int((current_index / total) * 100)
    current_stop = min(done_stop + max(int(100 / (total * 2)), 8), 100)
    return f"{done_stop}%", f"{current_stop}%"


def render(config: dict[str, Any], output: Path) -> str:
    config = normalize_config(config, output)
    state_data = build_state_data(config)
    current_detail = state_data[config["current"]]
    done_stop, current_stop = progress_stops(config)
    replacements = {
        "__DASHBOARD_TITLE__": esc(config["title"]),
        "__DASHBOARD_SUBTITLE__": esc(config["subtitle"]),
        "__ABS_HTML_PATH__": esc(config["outputPath"]),
        "__CURRENT_STATE_ID__": esc(config["current"]),
        "__CURRENT_STATE_TITLE__": esc(current_detail["title"]),
        "__DONE_STOP__": done_stop,
        "__CURRENT_STOP__": current_stop,
        "__FLOW_STEPS__": build_flow(config),
        "__DETAIL_KICKER__": esc(current_detail["kicker"]),
        "__DETAIL_TITLE__": esc(current_detail["title"]),
        "__DETAIL_BODY__": esc(current_detail["body"]),
        "__DETAIL_WHY__": esc(current_detail["why"]),
        "__DETAIL_EVIDENCE__": esc(current_detail["evidence"]),
        "__DETAIL_EXIT__": esc(current_detail["exit"]),
        "__RECENT_EVENTS__": build_recent(config),
        "__STATE_DATA_JSON__": json.dumps(state_data, ensure_ascii=False, indent=2),
    }
    html_text = TEMPLATE_PATH.read_text(encoding="utf-8")
    for key, value in replacements.items():
        html_text = html_text.replace(key, value)
    return html_text


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="State-machine JSON config.")
    parser.add_argument("--output", type=Path, required=True, help="Output HTML file.")
    parser.add_argument("--write-example", type=Path, help="Write an example JSON config before rendering.")
    args = parser.parse_args()

    if args.write_example:
        args.write_example.parent.mkdir(parents=True, exist_ok=True)
        args.write_example.write_text(json.dumps(EXAMPLE_CONFIG, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        config = EXAMPLE_CONFIG
    elif args.input:
        config = json.loads(args.input.read_text(encoding="utf-8"))
    else:
        raise SystemExit("Provide --input or --write-example")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(config, args.output) + "\n", encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
