
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, get_db
from .routers import cities, weather_info
from . import models

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

# FUTURE: User login capability
# FUTURE: Endpoints should have dependencies on the current_user for security and tracking

app.include_router(cities.router)
app.include_router(weather_info.router)


@app.get("/health")
def root():
    # TODO: test db connection
    return {"message": "I am a healthy boiiii"}

# FUTURE: Maybe expose a GET /excel post MVP for some of a get for large excel files? Currently decided to handle on client side
# that way we can serach up basic analytics insights from pandas and such as well to the user
