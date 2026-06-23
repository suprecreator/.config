#!/usr/bin/env python3
"""Small local save server for editable DasHTML dashboards."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any


def is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


class SaveHandler(BaseHTTPRequestHandler):
    server: "SaveServer"

    def log_message(self, fmt: str, *args: Any) -> None:
        print("%s - %s" % (self.log_date_time_string(), fmt % args), flush=True)

    def _headers(self, status: int = 200, content_type: str = "application/json") -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _json(self, status: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._headers(status)
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self._headers(204)

    def do_GET(self) -> None:
        if self.path != "/health":
            self._json(404, {"ok": False, "error": "not found"})
            return
        self._json(200, {
            "ok": True,
            "roots": [str(root) for root in self.server.allowed_roots],
        })

    def do_POST(self) -> None:
        if self.path != "/save":
            self._json(404, {"ok": False, "error": "not found"})
            return

        try:
            length = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
            target = Path(payload["path"]).expanduser().resolve()
            html = payload["html"]
            if not isinstance(html, str):
                raise ValueError("html must be a string")
            if not target.name.endswith(".html"):
                raise ValueError("target must be an .html file")
            if not any(is_relative_to(target, root) for root in self.server.allowed_roots):
                raise ValueError("target is outside allowed roots")

            target.parent.mkdir(parents=True, exist_ok=True)
            fd, tmp_name = tempfile.mkstemp(prefix=target.name + ".", suffix=".tmp", dir=target.parent)
            with os.fdopen(fd, "w", encoding="utf-8") as tmp:
                tmp.write(html)
                tmp.write("\n")
            os.replace(tmp_name, target)
            self._json(200, {"ok": True, "path": str(target), "bytes": len(html.encode("utf-8"))})
        except Exception as exc:
            self._json(400, {"ok": False, "error": str(exc)})


class SaveServer(ThreadingHTTPServer):
    def __init__(self, server_address: tuple[str, int], handler: type[SaveHandler], roots: list[Path]):
        super().__init__(server_address, handler)
        self.allowed_roots = roots


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a local DasHTML save server.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    parser.add_argument("--root", action="append", default=[], help="Allowed write root. Repeatable.")
    args = parser.parse_args()

    roots = [Path(root).expanduser().resolve() for root in args.root]
    if not roots:
        roots = [Path.cwd().resolve()]

    server = SaveServer((args.host, args.port), SaveHandler, roots)
    print(
        "DasHTML save server listening on http://%s:%d; roots=%s"
        % (args.host, args.port, ", ".join(str(root) for root in roots)),
        flush=True,
    )
    server.serve_forever()


if __name__ == "__main__":
    main()
