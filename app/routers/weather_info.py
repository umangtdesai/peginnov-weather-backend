from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List, Optional
from .. import models, schemas
from ..services.weather_service import WeatherService
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Weather Info"])

# FUTURE: add a city id as well, so we can do it per city vs. making so many API calls


@router.get("/weather/current", status_code=status.HTTP_200_OK, response_model=List[schemas.WeatherInfo])
async def get_current_weather_for_cities(
    db: Session = Depends(get_db)
):
    weather_and_city_info = []
    cities = db.query(models.City).order_by(
        models.City.created_at.desc()).all()  # recently created at the top
    for city in cities:

        # FUTURE: DRY Code.
        # FUTURE: some sort of worker based async process instead using Celery?
        weather = await WeatherService.get_current_weather(city.lat, city.lon)

        weather_and_city_info.append({
            "name": city.name,
            "country": city.country,
            "lat": city.lat,
            "lon": city.lon,
            "temperature": weather.temperature,
            "description": weather.description,
            "main_weather": weather.main_weather,
            "raw_api_response": weather.raw_api_response,
            "icon_code": weather.icon_code,
            "timestamp": weather.timestamp
        })

    return weather_and_city_info

# FUTURE: add a city id as well, so we can do it per city vs. making so many API calls
# FUTURE: let users specify date ranges


@router.get("/weather/historic", status_code=status.HTTP_200_OK, response_model=List[schemas.WeatherInfo])
async def get_historical_weather_for_cities(
    days: int = Query(default=3),
    db: Session = Depends(get_db)
):
    weather_and_city_info = []
    cities = db.query(models.City).order_by(
        models.City.created_at.desc()).all()  # recently created at the top
    # FUTURE: some sort of worker based async process instead using Celery?
    # NOTE: this logic should be well isolated in the service layer for the future
    for city in cities:
        for day in range(1, days + 1):  # 1 day ago until days day ago
            # this is better than 12am because you can compare weather at an exact point in time
            date = datetime.now() - timedelta(days=day)
            weather = await WeatherService.get_historical_weather(city.lat, city.lon, date)
            weather_and_city_info.append({
                "name": city.name,
                "country": city.country,
                "lat": city.lat,
                "lon": city.lon,
                "temperature": weather.temperature,
                "description": weather.description,
                "main_weather": weather.main_weather,
                "raw_api_response": weather.raw_api_response,
                "icon_code": weather.icon_code,
                "timestamp": weather.timestamp
            })

    return weather_and_city_info
