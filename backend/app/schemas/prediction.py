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


class PredictRequest(BaseModel):
    """Input features for the ML prediction model."""
    temperature: float
    humidity: float
    pressure: float
    wind_speed: float = 0.0
    wind_direction: float = 0.0
    visibility: float = 10.0
    month: int = 1
    hour: int = 12


class PredictResponse(BaseModel):
    """Result returned by the ML prediction model."""
    prediction: str
    score: float

