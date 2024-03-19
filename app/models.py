from .database import Base
from sqlalchemy import JSON, TIMESTAMP, Column, Float, ForeignKey, Integer, String, text

# FUTURE: Uniquness constraint + index missing
class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

# FUTURE: maybe unique on city_id and some sort of "weather_at"?
class WeatherInfo(Base):
    __tablename__ = "weather_info"

    id = Column(Integer, primary_key=True, nullable=False)
    city_id = Column(Integer, ForeignKey("cities.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False)
    temperature = Column(Integer) # store as kelvin, do converstion ourselves
    main_weather = Column(String, nullable=True)
    description=Column(String, nullable=True)
    icon_code=Column(String, nullable=True)
    raw_api_response = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# FUTURE: Users, Preferences, Other Weather data from the endpoints, Forecast, Alerts, etc 
# FUTURE: Consider using Mongo fo some portions of denormalized data
