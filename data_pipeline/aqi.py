# Modified by Aadil Mansuri
from datetime import datetime
from random import Random
import os

import requests

API_KEY = os.getenv("AQI_API_KEY") or os.getenv("WEATHER_API_KEY")

CITY_COORDS = {
    "Jaipur": (26.9124, 75.7873),
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
}


def _aqi_band(aqi: int) -> str:
    if aqi <= 50:
        return "Good"
    if aqi <= 100:
        return "Moderate"
    if aqi <= 150:
        return "Unhealthy for Sensitive"
    if aqi <= 200:
        return "Unhealthy"
    return "Very Unhealthy"


def _seed_for_city(city: str) -> int:
    hour_key = datetime.utcnow().strftime("%Y%m%d%H")
    return int(hour_key) * 7 + sum(ord(ch) for ch in city.lower())


def _mock_aqi(city: str) -> dict:
    rng = Random(_seed_for_city(city))
    aqi = int(rng.randint(55, 190))
    return {
        "city": city,
        "aqi": aqi,
        "aqi_band": _aqi_band(aqi),
        "source": "mock",
    }


def _convert_owm_scale_to_aqi(owm_aqi: int) -> int:
    scale_map = {1: 40, 2: 75, 3: 125, 4: 175, 5: 250}
    return scale_map.get(owm_aqi, 120)


def get_aqi(city: str, timeout: int = 6) -> dict:
    coords = CITY_COORDS.get(city)
    if not API_KEY or not coords:
        return _mock_aqi(city)

    lat, lon = coords
    url = (
        "https://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        owm_aqi = int(payload["list"][0]["main"]["aqi"])
        aqi = _convert_owm_scale_to_aqi(owm_aqi)
        return {
            "city": city,
            "aqi": aqi,
            "aqi_band": _aqi_band(aqi),
            "source": "openweathermap",
        }
    except Exception:
        return _mock_aqi(city)
