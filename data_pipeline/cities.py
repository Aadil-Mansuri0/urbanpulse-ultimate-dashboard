from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import pandas as pd


@dataclass(frozen=True)
class CityInfo:
    name: str
    lat: float
    lon: float


CITY_CATALOG: dict[str, CityInfo] = {
    "Jaipur": CityInfo("Jaipur", 26.9124, 75.7873),
    "Delhi": CityInfo("Delhi", 28.6139, 77.2090),
    "Mumbai": CityInfo("Mumbai", 19.0760, 72.8777),
    "Bengaluru": CityInfo("Bengaluru", 12.9716, 77.5946),
    "Hyderabad": CityInfo("Hyderabad", 17.3850, 78.4867),
    "Chennai": CityInfo("Chennai", 13.0827, 80.2707),
}


def get_available_cities() -> list[str]:
    return list(CITY_CATALOG.keys())


def get_city_coordinates(city: str) -> tuple[float, float]:
    info = CITY_CATALOG.get(city)
    if not info:
        raise ValueError(f"Unknown city: {city}")
    return info.lat, info.lon


def build_city_reference_frame(cities: Iterable[str] | None = None) -> pd.DataFrame:
    selected = list(cities) if cities else get_available_cities()
    rows = []
    for city in selected:
        info = CITY_CATALOG.get(city)
        if not info:
            continue
        rows.append({"city": info.name, "lat": info.lat, "lon": info.lon})
    return pd.DataFrame(rows)
