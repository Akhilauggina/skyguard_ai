from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.crud.station import create_station, get_all_stations
from app.db.dependencies import get_db
from app.schemas.station import StationCreate, StationResponse

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