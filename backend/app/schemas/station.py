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