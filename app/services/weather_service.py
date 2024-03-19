from typing import Optional

from fastapi import HTTPException, status
from app import schemas
from ..clients.weather_client import WeatherClient
from datetime import datetime


class WeatherService:
    client = WeatherClient()
        
    @classmethod
    async def fetch_weather_info(cls, city_id: int, lat: float, lon: float, timestamp: datetime = None) -> schemas.WeatherInfoRequest:
        """
            If timestamp is provided, get the historical weather info, else get current weather
        """
        if timestamp:
            weather_data = await WeatherService.get_historical_weather(lat, lon, timestamp)
            if not weather_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No historical weather data found for city ID {city_id} at timestamp {timestamp}"
                )
        else:
            weather_data = await WeatherService.get_current_weather(lat, lon)
            if not weather_data:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No current weather data found for city ID {city_id}"
                )

        return weather_data

    @classmethod
    async def get_historical_weather(cls, lat: float, lon: float, timestamp: datetime) -> Optional[schemas.WeatherInfoRequest]:
        try:
            historical_weather = await cls.client.get_historical_weather(lat, lon, timestamp)
            return historical_weather
    
        except Exception as e:
            return None
        
    @classmethod
    async def get_current_weather(cls, lat: float, lon: float) -> Optional[schemas.WeatherInfoRequest]:
        try:
            current_weather = await cls.client.get_current_weather(lat, lon)
            return current_weather
        
        except Exception as e:
            return None
