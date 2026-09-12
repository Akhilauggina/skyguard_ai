from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class PredictionBase(BaseModel):
    reading_id: int
    is_anomaly: bool
    confidence_score: float
    severity: str = "LOW"
    root_cause: Optional[str] = None
    explanation: Optional[str] = None
    model_name: str
    model_version: str
    inference_time_ms: Optional[float] = None
    created_at: Optional[datetime] = None


class PredictionCreate(PredictionBase):
    pass


class PredictionUpdate(BaseModel):
    reading_id: Optional[int] = None
    is_anomaly: Optional[bool] = None
    confidence_score: Optional[float] = None
    severity: Optional[str] = None
    root_cause: Optional[str] = None
    explanation: Optional[str] = None
    model_name: Optional[str] = None
    model_version: Optional[str] = None
    inference_time_ms: Optional[float] = None
    created_at: Optional[datetime] = None


class PredictionResponse(PredictionBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

