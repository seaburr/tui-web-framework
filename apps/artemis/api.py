"""
Artemis II telemetry API handler.

Routes:
  GET /api/artemis/telemetry   -> proxied NASA GCS JSON, 30-second cache
"""

import sys
import time
import threading
from pathlib import Path

# Allow importing lib.py from the framework root
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from lib import api_fetch

# ─── CONFIG ───────────────────────────────────────────────────────────────────
NASA_URL = (
    "https://storage.googleapis.com/download/storage/v1/b/p-2-cen1"
    "/o/October%2F1%2FOctober_105_1.txt?alt=media"
)
CACHE_TTL = 30  # seconds — NASA updates every ~4 min, so this is plenty fresh

# ─── CACHE ────────────────────────────────────────────────────────────────────
_cache: dict | None = None
_cache_ts: float = 0.0
_lock = threading.Lock()


def handle(path_parts: list[str]) -> tuple[int, dict, dict]:
    """
    Handle /api/artemis/<path_parts>.

    path_parts[0] must be "telemetry".

    Returns (status_code, body_dict, extra_headers).
    """
    global _cache, _cache_ts

    if not path_parts or path_parts[0] != "telemetry":
        return 404, {"error": "Not found"}, {}

    with _lock:
        if _cache and (time.time() - _cache_ts) < CACHE_TTL:
            return 200, _cache, {"X-Cache": "HIT"}

    data = api_fetch(NASA_URL)

    with _lock:
        _cache    = data
        _cache_ts = time.time()

    return 200, data, {"X-Cache": "MISS"}
