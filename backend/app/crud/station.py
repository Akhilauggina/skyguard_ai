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