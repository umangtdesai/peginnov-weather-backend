from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from .. import models, schemas
from ..services.geocoding_service import GeocodingService
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=["Cities"])


@router.get("/cities", status_code=status.HTTP_200_OK, response_model=List[schemas.CityGet])
def get_cities(db: Session = Depends(get_db)):
    # recently created to the right
    return db.query(models.City).order_by(models.City.created_at).all()

# IDEA: currently, defaulting the limit to 3 downstream, we can extend this later if the user needs some sort of "show more functionality"
# IDEA: We won't need it if we change the ui to more sane things (autocomplete to find right city using Google's API)


@router.get("/cities/search", status_code=status.HTTP_200_OK, response_model=List[schemas.City])
async def search_city(city: str = Query(...)):
    return await GeocodingService.search_city(city)

# TODO: Data normalization on POSTS


@router.post("/cities", status_code=status.HTTP_201_CREATED, response_model=schemas.CityPost)
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


@router.delete("/cities/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_city(city_id: int, db: Session = Depends(get_db)):
    city = db.query(models.City).filter(models.City.id == city_id).first()
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"City with ID {city_id} not found"
        )

    db.delete(city)
    db.commit()
