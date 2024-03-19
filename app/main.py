
from datetime import datetime
from typing import List, Optional
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware

from app.services.weather_service import WeatherService

from .services.geocoding_service import GeocodingService
from .database import engine, get_db
from . import models, schemas
from sqlalchemy.orm import Session

app = FastAPI(title="PEG Brain Weather Service", version="1.0.0")

# FUTURE: Use Alembic Migrations for DB creation instead
models.Base.metadata.create_all(bind=engine)

# FUTURE: This is a bit too open, we should restrict this to the frontend's domain
# FUTURE: Authentication endpoints
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# FUTURE: Create separate routers for cities and weather_info resources
# FUTURE: User login capability
# FUTURE: Endpoints should have dependencies on the current_user for security and tracking

#  ***** Cities  ******

# IDEA: currently, defaulting the limit to 3 downstream, we can extend this later if the user needs some sort of "show more functionality"
# IDEA: We won't need it if we change the ui to more sane things (autocomplete to find right city using Google's API)
@app.get("/cities/search", status_code=status.HTTP_200_OK, response_model=List[schemas.City])
async def search_city(city: str = Query(...)):
    return await GeocodingService.search_city(city)

# TODO: Data normalization on POSTS
@app.post("/cities", status_code=status.HTTP_201_CREATED, response_model=schemas.CityPost)
def create_city(city: schemas.City, db: Session = Depends(get_db)):
    # Only for ergonimics right now, not for prod code
    existing_city = db.query(models.City).filter(
        models.City.name == city.name,
        models.City.country == city.country,
        models.City.lat == city.lat
    ).first()

    if existing_city is not None:
        return schemas.CityPost(id=existing_city.id)


    # FUTURE: DB transactions in their own DAOs
    new_city = models.City(**city.model_dump())
    db.add(new_city)
    db.commit()
    db.refresh(new_city)

    return schemas.CityPost(id=new_city.id)


#  ***** Weather Info  ******

# FUTURE: handle "give me the data for the last 7 days" since we need to make 7 separate requests
@app.post("/weather", status_code=status.HTTP_204_NO_CONTENT)
async def create_weather_info_for_cities(
    city_ids: List[int] = Query(...),
    timestamp: Optional[datetime] = Query(None),
    db: Session = Depends(get_db)
):

    for city_id in city_ids:
        city = db.query(models.City).filter(models.City.id == city_id).first()
        if not city:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"City with ID {city_id} not found"
            )

        # FUTURE:
        # 1. Ensure that same timestamp + same city_id doesn't exist in the db
        # 2. some sort of worker based async process instead using Celery?
        weather_data = await WeatherService.fetch_weather_info(city_id, city.lat, city.lon, timestamp)

        new_weather_info = models.WeatherInfo(**weather_data.model_dump(), city_id=city_id)
        db.add(new_weather_info)

    db.commit()

# FUTURE: Pagination since, well, lots of data 
@app.get("/weather", status_code=status.HTTP_200_OK, response_model=List[schemas.WeatherInfo])
def get_weather_and_city_info(
    db: Session = Depends(get_db)
):
    weather_info = db.query(
        models.WeatherInfo, models.City
    ).join(
        models.City, models.WeatherInfo.city_id == models.City.id
    ).order_by(
        models.WeatherInfo.created_at.desc()
    ).all()

    weather_and_city_info = []
    for weather, city in weather_info:
        weather_and_city_info.append({
            "timestamp": weather.timestamp,
            "name": city.name,
            "country": city.country,
            "lat": city.lat,
            "lon": city.lon,
            "temperature": weather.temperature,
            "description": weather.description,
            "main_weather": weather.main_weather,
            "raw_api_response": weather.raw_api_response,
            "icon_code": weather.icon_code
        })

    return weather_and_city_info

@app.get("/health")
def root():
    # TODO: test db connection 
    return { "message": "I am a healthy boiiii" }

# FUTURE: Maybe expose a GET /excel post MVP for some of a get for large excel files? Currently decided to handle on client side
# that way we can serach up basic analytics insights from pandas and such as well to the user
