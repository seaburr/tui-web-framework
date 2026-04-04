# Adding Apps to tui-web-framework

An "app" is a directory under `apps/` with at minimum an `index.html`. Optionally it
has an `api.py` for server-side data fetching.

---

## Minimal example (static-only app)

```
apps/
  hello/
    index.html
```

That's it. The server automatically serves `index.html` at `/hello/` and `/hello/<anything>`.
The HTML can be a fully standalone page or it can link to the shared stylesheet:

```html
<link rel="stylesheet" href="/artemis-ui.css">
```

---

## App with a server-side API

Create `apps/<name>/api.py` exporting a single `handle` function:

```python
# apps/myapp/api.py

def handle(path_parts: list[str]) -> tuple[int, dict, dict]:
    """
    Called for every request to /api/myapp/...

    Args:
        path_parts: URL components *after* /api/myapp/
                    e.g. /api/myapp/foo/bar  ->  ['foo', 'bar']

    Returns:
        (status_code, response_body_dict, extra_headers_dict)
    """
    return 200, {"hello": "world"}, {}
```

The server discovers and loads all `api.py` files at startup — no registration step needed.

Use `lib.api_fetch` for outbound HTTP (it sets the correct User-Agent automatically):

```python
from lib import api_fetch

def handle(path_parts):
    data = api_fetch("https://example.com/some/json")
    return 200, data, {}
```

---

## Caching pattern

For APIs that call external services, use this three-tier pattern to avoid redundant calls:

```python
import time, threading
from lib import api_fetch

# Permanent cache (data that never changes — e.g. geocoding results)
_static_cache: dict = {}

# TTL cache (data that changes over time)
_live_cache: dict = {}
CACHE_TTL = 10 * 60  # seconds

_lock = threading.Lock()


def _get_static(key: str) -> dict:
    with _lock:
        if key in _static_cache:
            return _static_cache[key]
    data = api_fetch(f"https://example.com/static/{key}")
    with _lock:
        _static_cache[key] = data
    return data


def _get_live(key: str) -> tuple[dict, bool]:
    with _lock:
        entry = _live_cache.get(key)
        if entry and (time.time() - entry["ts"]) < CACHE_TTL:
            return entry["data"], True
    data = api_fetch(f"https://example.com/live/{key}")
    with _lock:
        _live_cache[key] = {"data": data, "ts": time.time()}
    return data, False


def handle(path_parts):
    if not path_parts:
        return 400, {"error": "key required"}, {}
    key = path_parts[0]
    data, cached = _get_live(key)
    return 200, data, {"X-Cache": "HIT" if cached else "MISS"}
```

---

## Client-side: reading the URL parameter

When the server routes `/weather/30002` to `apps/weather/index.html`, the zip code
lives in `window.location.pathname`. Read it like this:

```js
const parts = window.location.pathname.split('/').filter(Boolean);
// parts[0] = 'weather', parts[1] = '30002'
const param = parts[1] ?? '';
```

---

## File structure reference

```
tui-web-framework/
  artemis-ui.css          Shared stylesheet — link with /artemis-ui.css
  lib.py                  Shared Python helpers (api_fetch, UA constant)
  server.py               Router — do not edit to add apps
  Dockerfile
  .do/app.yaml
  apps/
    <name>/
      index.html          Required — served at /<name>/ and /<name>/<param>
      api.py              Optional — handle() called for /api/<name>/...
```

---

## Keeping the Artemis dashboard in sync

`apps/artemis/index.html` is a vendored copy of the Artemis II dashboard from the
[seaburr/artemis-tracker](https://github.com/seaburr/artemis-tracker) repo.
When that repo is updated, copy the file over manually or add a CI step:

```bash
cp ../artemis/index.html apps/artemis/index.html
```

The file fetches its data from `/api/artemis/telemetry`, which is handled by
`apps/artemis/api.py`.
