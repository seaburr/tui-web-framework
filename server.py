#!/usr/bin/env python3
"""
tui-web-framework server

Routing:
  GET /artemis-ui.css       -> static CSS framework
  GET /<app>                -> apps/<app>/index.html
  GET /<app>/<param>        -> apps/<app>/index.html  (param read by client JS)
  GET /api/<app>/...        -> apps/<app>/api.py handle()
  GET /healthz              -> health check

Adding an app:
  1. Create apps/<name>/index.html
  2. Optionally create apps/<name>/api.py with a handle() function
  See ADDING_APPS.md for details.
"""

import importlib.util
import json
import os
import sys
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

PORT     = int(os.environ.get("PORT", 8080))
BASE_DIR = Path(__file__).parent

# ─── APP API DISCOVERY ────────────────────────────────────────────────────────
# At startup, load any apps/<name>/api.py modules and register them by app name.
# Each module must export: handle(path_parts: list[str]) -> (int, dict, dict)

_app_apis: dict[str, object] = {}

def _load_app_apis() -> None:
    apps_dir = BASE_DIR / "apps"
    if not apps_dir.exists():
        return
    for app_dir in sorted(apps_dir.iterdir()):
        api_file = app_dir / "api.py"
        if not api_file.exists():
            continue
        spec = importlib.util.spec_from_file_location(
            f"apps.{app_dir.name}.api", api_file
        )
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            _app_apis[app_dir.name] = mod
            print(f"[startup] Loaded API: {app_dir.name}", flush=True)
        except Exception as e:
            print(f"[startup] Failed to load API for {app_dir.name}: {e}", flush=True)


# ─── STATIC FILE CACHE ────────────────────────────────────────────────────────
_static_cache: dict[Path, bytes] = {}

def _read_static(file_path: Path) -> bytes:
    if file_path not in _static_cache:
        _static_cache[file_path] = file_path.read_bytes()
    return _static_cache[file_path]


# ─── REQUEST HANDLER ─────────────────────────────────────────────────────────
class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        print(
            f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] "
            f"{self.address_string()} {fmt % args}",
            flush=True,
        )

    def do_GET(self):
        url_path = self.path.split("?")[0].rstrip("/") or "/"
        parts    = [p for p in url_path.split("/") if p]

        # -- /healthz --
        if url_path == "/healthz":
            self._send(200, "text/plain", b"ok")
            return

        # -- /artemis-ui.css --
        if url_path == "/artemis-ui.css":
            css_path = BASE_DIR / "artemis-ui.css"
            if css_path.exists():
                self._send(200, "text/css", _read_static(css_path),
                           extra={"Cache-Control": "public, max-age=300"})
            else:
                self._send(404, "text/plain", b"Not found")
            return

        # -- /api/<app>/... --
        if len(parts) >= 2 and parts[0] == "api":
            app_name  = parts[1]
            sub_parts = parts[2:]
            if app_name in _app_apis:
                try:
                    status, data, extra = _app_apis[app_name].handle(sub_parts)
                except Exception as e:
                    status, data, extra = 500, {"error": str(e)}, {}
                self._json(status, data, extra=extra or None)
            else:
                self._json(404, {"error": f"No API registered for '{app_name}'"})
            return

        # -- /<app>  or  /<app>/<param> --
        if parts:
            app_html = BASE_DIR / "apps" / parts[0] / "index.html"
            if app_html.exists():
                self._send(200, "text/html", _read_static(app_html))
                return

        # -- / -> app listing --
        if url_path == "/":
            apps_dir = BASE_DIR / "apps"
            apps = sorted(
                d.name for d in apps_dir.iterdir()
                if d.is_dir() and (d / "index.html").exists()
            ) if apps_dir.exists() else []
            body = "TUI WEB FRAMEWORK\n\nAvailable apps:\n"
            body += "\n".join(f"  /{a}/" for a in apps) + "\n"
            self._send(200, "text/plain", body.encode())
            return

        self._send(404, "text/plain", b"Not found")

    def _send(self, status: int, content_type: str, body: bytes,
              extra: dict | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        for k, v in (extra or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def _json(self, status: int, data: dict,
              extra: dict | None = None) -> None:
        self._send(status, "application/json", json.dumps(data).encode(), extra=extra)


# ─── ENTRY POINT ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    _load_app_apis()
    server = ThreadingHTTPServer(("", PORT), Handler)
    print(
        f"[{time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}] "
        f"tui-web-framework listening on :{PORT}",
        flush=True,
    )
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        sys.exit(0)
