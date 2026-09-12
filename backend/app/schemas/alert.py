from datetime import datetime
from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    station_id: int
    message: str
    severity: str
    status: str


class AlertUpdate(BaseModel):
    message: str | None = None
    severity: str | None = None
    status: str | None = None


class AlertResponse(AlertCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)