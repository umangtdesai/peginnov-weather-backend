from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

WEATHER_SERVICE_DB_USERNAME = os.getenv("DB_USER", "postgres") # database-1.cbag4ayeizn4.us-east-1.rds.amazonaws.com
WEATHER_SERVICE_DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
WEATHER_SERVICE_DB_HOST = os.getenv("DB_HOST", "localhost")
WEATHER_SERVICE_DB_PORT = os.getenv("DB_PORT", "5433") # RDS = 5432, docker = 5432, local = 5433
WEATHER_SERVICE_DB = os.getenv("DB_NAME", "weather_app_db") # same in RDS

# FUTUE: if multiple data source / need better "unstructuring" move to mongo like non-relational db
SQLALCHEMY_DATABASE_URL = f"postgresql://{WEATHER_SERVICE_DB_USERNAME}:{WEATHER_SERVICE_DB_PASSWORD}@{WEATHER_SERVICE_DB_HOST}:{WEATHER_SERVICE_DB_PORT}/{WEATHER_SERVICE_DB}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
