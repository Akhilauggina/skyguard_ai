from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.station import Station
from app.models.weather_reading import WeatherReading
from app.schemas.weather_reading import WeatherReadingCreate, WeatherReadingUpdate


def create_weather_reading(
    db: Session,
    reading: WeatherReadingCreate,
) -> WeatherReading:
    # Verify that the referenced station exists
    station = db.query(Station).filter(Station.id == reading.station_id).first()
    if station is None:
        raise HTTPException(
            status_code=404,
            detail=f"Station with id {reading.station_id} not found",
        )

    db_reading = WeatherReading(**reading.model_dump())

    db.add(db_reading)
    db.commit()
    db.refresh(db_reading)

    return db_reading


def get_all_weather_readings(db: Session) -> list[WeatherReading]:
    return db.query(WeatherReading).all()


def get_weather_reading_by_id(db: Session, reading_id: int) -> WeatherReading:
    reading = db.query(WeatherReading).filter(WeatherReading.id == reading_id).first()
    if reading is None:
        raise HTTPException(
            status_code=404,
            detail="Weather reading not found",
        )
    return reading


def update_weather_reading(
    db: Session,
    reading_id: int,
    reading_data: WeatherReadingUpdate,
) -> WeatherReading:
    db_reading = get_weather_reading_by_id(db, reading_id)

    update_data = reading_data.model_dump(exclude_unset=True)

    # If updating station_id, verify that new station exists
    if "station_id" in update_data and update_data["station_id"] is not None:
        station = db.query(Station).filter(Station.id == update_data["station_id"]).first()
        if station is None:
            raise HTTPException(
                status_code=404,
                detail=f"Station with id {update_data['station_id']} not found",
            )

    for key, value in update_data.items():
        setattr(db_reading, key, value)

    db.commit()
    db.refresh(db_reading)

    return db_reading


def delete_weather_reading(db: Session, reading_id: int) -> dict:
    db_reading = get_weather_reading_by_id(db, reading_id)

    db.delete(db_reading)
    db.commit()

    return {"message": "Weather reading deleted successfully"}


def get_station_readings(
    db: Session,
    station_id: int,
) -> list[WeatherReading]:
    # Verify station exists
    station = db.query(Station).filter(Station.id == station_id).first()
    if station is None:
        raise HTTPException(
            status_code=404,
            detail=f"Station with id {station_id} not found",
        )

    return (
        db.query(WeatherReading)
        .filter(WeatherReading.station_id == station_id)
        .all()
    )
