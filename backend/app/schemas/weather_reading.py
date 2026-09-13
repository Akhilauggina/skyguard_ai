from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class WeatherReadingBase(BaseModel):
    station_id: int
    temperature: float
    pressure: float
    humidity: float
    recorded_at: datetime


class WeatherReadingCreate(WeatherReadingBase):
    pass


class WeatherReadingUpdate(BaseModel):
    station_id: Optional[int] = None
    temperature: Optional[float] = None
    pressure: Optional[float] = None
    humidity: Optional[float] = None
    recorded_at: Optional[datetime] = None


class WeatherReadingResponse(WeatherReadingBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class LiveWeatherResponse(BaseModel):
    """Response for live weather fetch endpoint."""

    weather: dict
    prediction: dict
