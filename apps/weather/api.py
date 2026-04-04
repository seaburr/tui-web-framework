"""
Weather API handler using NOAA/NWS.

Routes:
  GET /api/weather/<zip>   -> current conditions + forecast JSON

Caching (tiered):
  Geocoding (zip -> lat/lon):         permanent per process lifetime
  NWS points (lat/lon -> URLs):       permanent per process lifetime
  Live weather (observation/forecast): 10-minute TTL

After the first request for a given ZIP, subsequent refreshes only
make 2 network calls (observation + forecast) instead of 5.
"""

import sys
import time
import threading
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from lib import api_fetch

# ─── CONFIG ───────────────────────────────────────────────────────────────────
WEATHER_CACHE_TTL = 10 * 60  # seconds

# ─── CACHES ───────────────────────────────────────────────────────────────────
_geo_cache: dict[str, dict]     = {}   # zip  -> {lat, lon, city, state}       — permanent
_nws_cache: dict[str, dict]     = {}   # zip  -> {forecast_url, station_id, …} — permanent
_weather_cache: dict[str, dict] = {}   # zip  -> {data, ts}                    — 10 min TTL
_lock = threading.Lock()


# ─── FETCH HELPERS ────────────────────────────────────────────────────────────

def _fetch_geo(zip_code: str) -> dict:
    with _lock:
        if zip_code in _geo_cache:
            return _geo_cache[zip_code]

    url = (
        "https://nominatim.openstreetmap.org/search?"
        + urllib.parse.urlencode({
            "postalcode": zip_code,
            "country": "US",
            "format": "json",
            "limit": "1",
            "addressdetails": "1",
        })
    )
    results = api_fetch(url)
    if not results:
        raise ValueError(f"No location found for ZIP {zip_code}")
    g    = results[0]
    addr = g.get("address", {})
    geo  = {
        "lat":   float(g["lat"]),
        "lon":   float(g["lon"]),
        "city":  addr.get("city") or addr.get("town") or addr.get("village") or "",
        "state": addr.get("state", ""),
    }
    with _lock:
        _geo_cache[zip_code] = geo
    return geo


def _fetch_nws_points(zip_code: str, lat: float, lon: float) -> dict:
    with _lock:
        if zip_code in _nws_cache:
            return _nws_cache[zip_code]

    pts      = api_fetch(f"https://api.weather.gov/points/{lat:.4f},{lon:.4f}")
    props    = pts["properties"]
    rel      = props.get("relativeLocation", {}).get("properties", {})
    stations = api_fetch(props["observationStations"])

    if not stations.get("features"):
        raise ValueError("No observation stations found")
    station_id = stations["features"][0]["properties"]["stationIdentifier"]

    nws = {
        "forecast_url": props["forecast"],
        "station_id":   station_id,
        "city":         rel.get("city",  ""),
        "state":        rel.get("state", ""),
    }
    with _lock:
        _nws_cache[zip_code] = nws
    return nws


def _fetch_live_weather(forecast_url: str, station_id: str) -> tuple[dict, list]:
    obs = api_fetch(
        f"https://api.weather.gov/stations/{station_id}/observations/latest"
    )
    op = obs["properties"]

    def val(key):
        return (op.get(key) or {}).get("value")

    current = {
        "textDescription":    op.get("textDescription", ""),
        "temperature":        val("temperature"),          # degrees C
        "relativeHumidity":   val("relativeHumidity"),     # percent
        "windSpeed":          val("windSpeed"),             # m/s
        "windDirection":      val("windDirection"),         # degrees
        "barometricPressure": val("barometricPressure"),   # Pa
        "visibility":         val("visibility"),            # m
        "timestamp":          op.get("timestamp"),
    }

    fc      = api_fetch(forecast_url)
    periods = (fc.get("properties") or {}).get("periods", [])[:14]
    return current, periods


# ─── PUBLIC API ───────────────────────────────────────────────────────────────

def get_weather(zip_code: str) -> tuple[dict, bool]:
    """Return (data, from_cache). Thread-safe."""
    with _lock:
        entry = _weather_cache.get(zip_code)
        if entry and (time.time() - entry["ts"]) < WEATHER_CACHE_TTL:
            return entry["data"], True

    geo     = _fetch_geo(zip_code)
    nws     = _fetch_nws_points(zip_code, geo["lat"], geo["lon"])
    current, periods = _fetch_live_weather(nws["forecast_url"], nws["station_id"])

    data = {
        "location": {
            "city":    nws["city"]  or geo["city"],
            "state":   nws["state"] or geo["state"],
            "zip":     zip_code,
            "lat":     geo["lat"],
            "lon":     geo["lon"],
            "station": nws["station_id"],
        },
        "current":   current,
        "forecast":  periods,
        "fetchedAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    with _lock:
        _weather_cache[zip_code] = {"data": data, "ts": time.time()}

    return data, False


def handle(path_parts: list[str]) -> tuple[int, dict, dict]:
    """
    Handle /api/weather/<path_parts>.

    path_parts[0] must be a 5-digit ZIP code.

    Returns (status_code, body_dict, extra_headers).
    """
    if not path_parts:
        return 400, {"error": "ZIP code required — usage: /api/weather/30002"}, {}

    raw_zip = "".join(c for c in path_parts[0] if c.isdigit())[:5]
    if len(raw_zip) != 5:
        return 400, {"error": "Invalid ZIP code"}, {}

    data, cached = get_weather(raw_zip)
    return 200, data, {"X-Cache": "HIT" if cached else "MISS"}
