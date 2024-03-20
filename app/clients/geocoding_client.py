from typing import List
from fastapi import HTTPException, status
from app import schemas
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# FUTURE: base client that initializes the API key and loads env vars there


class GeocodingClient:
    BASE_URL = "http://api.openweathermap.org/geo/1.0/direct"
    DEFAULT_LIMIT = 3

    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")

    # FUTURE: Let users have show more functionality
    async def search_city(self, city: str, limit: int = DEFAULT_LIMIT) -> List[schemas.City]:
        params = {
            "q": f"{city}",
            "limit": limit,
            "appid": self.api_key
        }

        response = requests.get(self.BASE_URL, params=params)
        data = response.json()

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code,
                                detail=data.get("message", "Unknown error"))

        cities = []
        for city in data:
            new_city = schemas.City(
                name=city['name'], country=city['country'], lat=city['lat'], lon=city['lon'],)
            cities.append(new_city)

        return cities
