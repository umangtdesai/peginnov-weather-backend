from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from app import schemas
import requests
import os
from dotenv import load_dotenv

load_dotenv()


class WeatherClient:
    BASE_URL_CURRENT = "https://api.openweathermap.org/data/3.0/onecall"
    BASE_URL_HISTORICAL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

    def __init__(self):
        self.api_key = os.environ.get("OPENWEATHER_API_KEY")

    async def get_current_weather(self, lat: float, lon: float) -> schemas.WeatherInfoRequest:
        params = {
            "lat": lat,
            "lon": lon,
            "appid": self.api_key,
            # FUTURE: use forcast for insights and alerts
            "exclude": "minutely,hourly,daily,alerts"
        }

        response = requests.get(self.BASE_URL_CURRENT, params=params)
        data = response.json()

        if response.status_code != status.HTTP_200_OK:
            raise HTTPException(status_code=response.status_code,
                                detail=data.get("message", "Unknown error"))

        current_weather = schemas.WeatherInfoRequest(
            # for current weather, we don't have a timestamp, so we use the current time
            timestamp=data['current']['dt'],
            temperature=data['current']['temp'],
            description=data['current']['weather'][0]['description'],
            main_weather=data['current']['weather'][0]['main'],
            icon_code=data['current']['weather'][0]['icon'],
            raw_api_response=data
        )

        return current_weather

    # OpenWeather Notes: Please note that the one API response contains weather data for only one specified timestamp.
    # TODO: Front end validation, supported date: 1st January 1979 till 4 days ahead of today
    async def get_historical_weather(self, lat: float, lon: float, time: datetime) -> Optional[schemas.WeatherInfoRequest]:
        unix_time = int(time.timestamp())
        params = {
            "lat": lat,
            "lon": lon,
            "dt": unix_time,
            "appid": self.api_key
        }

        response = requests.get(self.BASE_URL_HISTORICAL, params=params)
        data = response.json()

        if response.status_code != status.HTTP_200_OK:
            # If data is not available for given time, return None
            if response.status_code == status.HTTP_404_NOT_FOUND:
                return None
            else:
                raise HTTPException(status_code=response.status_code, detail=data.get(
                    "message", "No data for the given date"))

        historical_weather = schemas.WeatherInfoRequest(
            timestamp=data['data'][0]['dt'],
            temperature=data['data'][0]['temp'],
            description=data['data'][0]['weather'][0]['description'],
            main_weather=data['data'][0]['weather'][0]['main'],
            icon_code=data['data'][0]['weather'][0]['icon'],
            raw_api_response=data
        )

        return historical_weather
