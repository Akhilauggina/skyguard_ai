from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.station import create_station, get_all_stations
from app.db.dependencies import get_db
from app.schemas.station import StationCreate, StationResponse
from app.crud.station import (
    create_station,
    get_all_stations,
    get_station_by_id,
    update_station,
    delete_station,
)

from app.schemas.station import (
    StationCreate,
    StationResponse,
    StationUpdate,
)
router = APIRouter(
    prefix="/stations",
    tags=["Stations"],
)


@router.post(
    "",
    response_model=StationResponse,
    status_code=201,
)
def create_new_station(
    station: StationCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new weather station.
    """
    return create_station(db, station)


@router.get(
    "",
    response_model=list[StationResponse],
)
def read_all_stations(
    db: Session = Depends(get_db),
):
    """
    Return all weather stations.
    """
    return get_all_stations(db)
@router.get("/{station_id}", response_model=StationResponse)
def get_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    return get_station_by_id(db, station_id)

@router.put("/{station_id}", response_model=StationResponse)
def edit_station(
    station_id: int,
    station: StationUpdate,
    db: Session = Depends(get_db),
):
    return update_station(db, station_id, station)

@router.delete("/{station_id}")
def remove_station(
    station_id: int,
    db: Session = Depends(get_db),
):
    return delete_station(db, station_id)