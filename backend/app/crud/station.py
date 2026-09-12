from sqlalchemy.orm import Session

from app.models.station import Station
from app.schemas.station import StationCreate


def create_station(db: Session, station: StationCreate) -> Station:
    """
    Create a new weather station.
    """

    db_station = Station(
        station_code=station.station_code,
        name=station.name,
        city=station.city,
        state=station.state,
        latitude=station.latitude,
        longitude=station.longitude,
        status=station.status,
        installation_date=station.installation_date,
        last_maintenance=station.last_maintenance,
    )

    db.add(db_station)
    db.commit()
    db.refresh(db_station)

    return db_station


def get_all_stations(db: Session):
    """
    Return all weather stations.
    """
    return db.query(Station).all()


from fastapi import HTTPException

from app.schemas.station import StationUpdate


def get_station_by_id(db: Session, station_id: int) -> Station:
    station = db.query(Station).filter(Station.id == station_id).first()

    if station is None:
        raise HTTPException(status_code=404, detail="Station not found")

    return station


def update_station(
    db: Session,
    station_id: int,
    station_data: StationUpdate,
) -> Station:

    station = get_station_by_id(db, station_id)

    update_data = station_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(station, key, value)

    db.commit()
    db.refresh(station)

    return station


def delete_station(db: Session, station_id: int):

    station = get_station_by_id(db, station_id)

    db.delete(station)

    db.commit()

    return {"message": "Station deleted successfully"}