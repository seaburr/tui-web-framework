"""
Shared utilities for app API handlers.

Usage in an api.py:
    from lib import api_fetch, UA
"""

import json
import urllib.request

UA = "tui-web-framework/1.0 (seaburr.io)"


def api_fetch(url: str) -> dict:
    """GET a JSON endpoint, raising on non-200 or network error."""
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())
