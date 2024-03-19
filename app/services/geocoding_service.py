from typing import List
from ..clients.geocoding_client import GeocodingClient
from app import schemas

class GeocodingService():
    client = GeocodingClient()

    @classmethod
    async def search_city(cls, city: str) -> List[schemas.City]:
        # FUTURE: handle exception so user gets a better error message
        return await cls.client.search_city(city)
