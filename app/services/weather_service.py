from typing import Optional

from app import schemas
from ..clients.weather_client import WeatherClient
from datetime import datetime


class WeatherService:
    client = WeatherClient()

    # FUTURE: Could dry up but better to have as service method per endpoint for now
    @classmethod
    async def get_historical_weather(cls, lat: float, lon: float, timestamp: datetime) -> Optional[schemas.WeatherInfoRequest]:
        try:
            historical_weather = await cls.client.get_historical_weather(lat, lon, timestamp)
            return historical_weather

        except Exception as e:
            raise e

    @classmethod
    async def get_current_weather(cls, lat: float, lon: float) -> Optional[schemas.WeatherInfoRequest]:
        try:
            current_weather = await cls.client.get_current_weather(lat, lon)
            return current_weather

        except Exception as e:
            raise e
