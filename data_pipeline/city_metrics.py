# Modified by Aadil Mansuri
from __future__ import annotations

from datetime import datetime
import math
from typing import Iterable

import pandas as pd

from data_pipeline.airport import get_airport_stats
from data_pipeline.aqi import get_aqi
from data_pipeline.cities import CITY_CATALOG, get_available_cities
from data_pipeline.flight import get_live_flights
from data_pipeline.population import get_population
from data_pipeline.weather import get_weather


def _normalize_temp_score(temp: float) -> float:
    # Ideal operational comfort band centered around 24C.
    return max(0.0, min(100.0, 100 - abs(temp - 24) * 4.8))


def _normalize_aqi_score(aqi: int) -> float:
    return max(0.0, min(100.0, 100 - (aqi - 30) * 0.45))


def _estimate_congestion(flights_active: int, population: int, airports: int) -> float:
    flight_pressure = min(100.0, flights_active * 0.6)
    population_pressure = min(100.0, population / 250000)
    infra_relief = min(35.0, airports * 12.0)
    congestion = flight_pressure * 0.55 + population_pressure * 0.45 - infra_relief
    return max(0.0, min(100.0, congestion))


def city_score(temp: float, aqi: int, flights_active: int, population: int, airports: int) -> float:
    temp_score = _normalize_temp_score(temp)
    aqi_score = _normalize_aqi_score(aqi)
    congestion = _estimate_congestion(flights_active, population, airports)
    infra_score = min(100.0, 45 + airports * 20)

    score = (
        temp_score * 0.30
        + aqi_score * 0.35
        + infra_score * 0.20
        + (100 - congestion) * 0.15
    )
    return round(max(0.0, min(100.0, score)), 2)


def _score_label(score: float) -> str:
    if score >= 80:
        return "Excellent"
    if score >= 65:
        return "Good"
    if score >= 50:
        return "Watch"
    return "Critical"


def _predict_temp_next_hour(temp: float, hour_context: int | None = None) -> float:
    hour = hour_context if hour_context is not None else datetime.now().hour
    swing = math.sin((hour + 1) * math.pi / 12) * 1.8
    return round(temp + swing, 1)


def build_city_metrics(
    cities: Iterable[str] | None = None,
    hour_override: int | None = None,
) -> pd.DataFrame:
    selected = list(cities) if cities else get_available_cities()
    rows = []

    for city in selected:
        if city not in CITY_CATALOG:
            continue

        weather = get_weather(city)
        aqi_data = get_aqi(city)
        airport = get_airport_stats(city)
        flights = get_live_flights(city)
        population = get_population(city)
        lat, lon = CITY_CATALOG[city].lat, CITY_CATALOG[city].lon

        congestion = _estimate_congestion(
            flights_active=int(flights["flights_active"]),
            population=population,
            airports=int(airport["airports"]),
        )
        health_score = city_score(
            temp=float(weather["temp"]),
            aqi=int(aqi_data["aqi"]),
            flights_active=int(flights["flights_active"]),
            population=population,
            airports=int(airport["airports"]),
        )

        rows.append(
            {
                "city": city,
                "lat": lat,
                "lon": lon,
                "population": population,
                "airports": int(airport["airports"]),
                "major_hub": airport["major_hub"],
                "temp": float(weather["temp"]),
                "temp_next_hour": _predict_temp_next_hour(float(weather["temp"]), hour_override),
                "weather": weather["weather"],
                "aqi": int(aqi_data["aqi"]),
                "aqi_band": aqi_data["aqi_band"],
                "flights": int(flights["flights_active"]),
                "avg_altitude": float(flights["avg_altitude"]),
                "congestion_index": round(congestion, 2),
                "city_health_score": health_score,
                "score_label": _score_label(health_score),
                "weather_source": weather.get("source", "unknown"),
                "aqi_source": aqi_data.get("source", "unknown"),
                "flights_source": flights.get("source", "unknown"),
                "observed_at": datetime.now().isoformat(timespec="seconds"),
            }
        )

    frame = pd.DataFrame(rows)
    if frame.empty:
        return frame

    frame = frame.sort_values("city_health_score", ascending=False).reset_index(drop=True)
    frame["rank"] = frame.index + 1
    return frame
