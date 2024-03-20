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

# FUTURE: Users, Preferences, Other Weather data from the endpoints, Forecast, Alerts, etc 
# FUTURE: Consider using Mongo fo some portions of denormalized data
