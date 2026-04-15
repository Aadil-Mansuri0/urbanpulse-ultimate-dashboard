from __future__ import annotations

from datetime import datetime
from random import Random

import requests

from data_pipeline.cities import get_city_coordinates


def _seed_for_city(city: str) -> int:
    hour_key = datetime.utcnow().strftime("%Y%m%d%H")
    return int(hour_key) * 13 + sum(ord(ch) for ch in city.lower())


def _mock_flights(city: str) -> dict:
    rng = Random(_seed_for_city(city))
    active = int(rng.randint(18, 220))
    avg_alt = int(rng.randint(3500, 10400))
    return {
        "city": city,
        "flights_active": active,
        "avg_altitude": avg_alt,
        "source": "mock",
    }


def get_live_flights(city: str, timeout: int = 5) -> dict:
    try:
        lat, lon = get_city_coordinates(city)
    except ValueError:
        return _mock_flights(city)

    bounds = {
        "lamin": lat - 1.2,
        "lomin": lon - 1.2,
        "lamax": lat + 1.2,
        "lomax": lon + 1.2,
    }

    try:
        response = requests.get(
            "https://opensky-network.org/api/states/all",
            params=bounds,
            timeout=timeout,
        )
        response.raise_for_status()
        payload = response.json()
        states = payload.get("states") or []

        if not states:
            return _mock_flights(city)

        altitudes = [
            float(state[7])
            for state in states
            if isinstance(state, list) and len(state) > 7 and state[7] is not None
        ]
        avg_altitude = int(sum(altitudes) / len(altitudes)) if altitudes else 0
        return {
            "city": city,
            "flights_active": len(states),
            "avg_altitude": avg_altitude,
            "source": "opensky",
        }
    except Exception:
        return _mock_flights(city)
