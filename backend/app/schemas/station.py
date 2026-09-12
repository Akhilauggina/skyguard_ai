from datetime import date
from typing import Optional

from pydantic import BaseModel, ConfigDict


class StationCreate(BaseModel):
    """Request schema for creating a weather station."""

    station_code: str
    name: str
    city: str
    state: str
    latitude: float
    longitude: float
    status: str = "ACTIVE"
    installation_date: date
    last_maintenance: Optional[date] = None


class StationResponse(BaseModel):
    """Response schema returned by the API."""

    id: int
    station_code: str
    name: str
    city: str
    state: str
    latitude: float
    longitude: float
    status: str
    installation_date: date
    last_maintenance: Optional[date]

    model_config = ConfigDict(from_attributes=True)

class StationUpdate(BaseModel):
    station_code: str | None = None
    name: str | None = None
    city: str | None = None
    state: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    status: str | None = None
    installation_date: date | None = None
    last_maintenance: date | None = None