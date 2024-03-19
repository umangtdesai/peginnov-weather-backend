from datetime import datetime
from pydantic import BaseModel
from typing import Dict

# Future: Pydantic offers a lot more validations + custom validations that can be used here.
class City(BaseModel):
    name: str
    country: str
    lat: float
    lon: float

class CityPost(BaseModel):
    id: int
    
class WeatherInfoBase(BaseModel):
    temperature: float
    description: str
    main_weather: str
    icon_code: str
    timestamp: datetime 

class WeatherInfoPost(BaseModel):
    id: int

class WeatherInfo(WeatherInfoBase):
    raw_api_response: Dict
    name: str
    country: str
    lat: float
    lon: float

class WeatherInfoRequest(WeatherInfoBase):
    raw_api_response: Dict
