CITY_POPULATION = {
    "Jaipur": 4100000,
    "Delhi": 32900000,
    "Mumbai": 21600000,
    "Bengaluru": 14100000,
    "Hyderabad": 11000000,
    "Chennai": 12100000,
}


def get_population(city: str) -> int:
    return int(CITY_POPULATION.get(city, 3000000))
