# Modified by Aadil Mansuri
from datetime import datetime
from random import Random
import os

import requests

API_KEY = os.getenv("WEATHER_API_KEY")


def _seed_for_city(city: str) -> int:
    hour_key = datetime.utcnow().strftime("%Y%m%d%H")
    return int(hour_key) + sum(ord(ch) for ch in city.lower())


def _mock_weather(city: str) -> dict:
    rng = Random(_seed_for_city(city))
    temp = round(rng.uniform(21, 39), 1)
    description = rng.choice([
        "clear sky",
        "few clouds",
        "scattered clouds",
        "haze",
        "light rain",
    ])
    return {
        "city": city,
        "temp": temp,
        "weather": description,
        "time": datetime.now().isoformat(timespec="seconds"),
        "source": "mock",
    }


def get_weather(city: str, timeout: int = 6) -> dict:
    if not API_KEY:
        return _mock_weather(city)

    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={API_KEY}&units=metric"
    )
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        payload = response.json()
        return {
            "city": city,
            "temp": round(float(payload["main"]["temp"]), 1),
            "weather": payload["weather"][0]["description"],
            "time": datetime.now().isoformat(timespec="seconds"),
            "source": "openweathermap",
        }
    except Exception:
        return _mock_weather(city)
