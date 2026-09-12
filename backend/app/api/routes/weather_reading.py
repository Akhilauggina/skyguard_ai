from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.weather_reading import (
    create_weather_reading,
    delete_weather_reading,
    get_all_weather_readings,
    get_station_readings,
    get_weather_reading_by_id,
    update_weather_reading,
)
from app.db.dependencies import get_db
from app.schemas.weather_reading import (
    WeatherReadingCreate,
    WeatherReadingResponse,
    WeatherReadingUpdate,
)

router = APIRouter(
    prefix="/weather-readings",
    tags=["Weather Readings"],
)


@router.post(
    "",
    response_model=WeatherReadingResponse,
    status_code=201,
    summary="Create a new weather reading",
)
def create_reading(
    reading: WeatherReadingCreate,
    db: Session = Depends(get_db),
):
    return create_weather_reading(db, reading)


@router.get(
    "",
    response_model=list[WeatherReadingResponse],
    summary="Get all weather readings",
)
def get_all_readings(
    db: Session = Depends(get_db),
):
    return get_all_weather_readings(db)


@router.get(
    "/station/{station_id}",
    response_model=list[WeatherReadingResponse],
    summary="Get all weather readings for a station",
)
def get_readings_by_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    return get_station_readings(db, station_id)


@router.get(
    "/{id}",
    response_model=WeatherReadingResponse,
    summary="Get a weather reading by ID",
)
def get_reading(
    id: int,
    db: Session = Depends(get_db),
):
    return get_weather_reading_by_id(db, id)


@router.put(
    "/{id}",
    response_model=WeatherReadingResponse,
    summary="Update a weather reading by ID",
)
def update_reading(
    id: int,
    reading: WeatherReadingUpdate,
    db: Session = Depends(get_db),
):
    return update_weather_reading(db, id, reading)


@router.delete(
    "/{id}",
    summary="Delete a weather reading by ID",
)
def delete_reading(
    id: int,
    db: Session = Depends(get_db),
):
    return delete_weather_reading(db, id)
