AIRPORT_DATA = {
    "Jaipur": {"airports": 1, "major_hub": "Jaipur International Airport"},
    "Delhi": {"airports": 2, "major_hub": "Indira Gandhi International Airport"},
    "Mumbai": {"airports": 2, "major_hub": "Chhatrapati Shivaji Maharaj International Airport"},
    "Bengaluru": {"airports": 1, "major_hub": "Kempegowda International Airport"},
    "Hyderabad": {"airports": 1, "major_hub": "Rajiv Gandhi International Airport"},
    "Chennai": {"airports": 1, "major_hub": "Chennai International Airport"},
}


def get_airport_stats(city: str) -> dict:
    fallback = {"airports": 1, "major_hub": f"{city} Airport"}
    data = AIRPORT_DATA.get(city, fallback)
    return {"city": city, **data}
