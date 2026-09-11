from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.weather_reading import WeatherReading
    from app.models.alert import Alert


class Prediction(Base):
    """AI prediction generated for a weather reading."""

    __tablename__ = "predictions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    reading_id: Mapped[int] = mapped_column(
        ForeignKey("weather_readings.id"),
        nullable=False,
        index=True,
    )

    is_anomaly: Mapped[bool] = mapped_column(Boolean, nullable=False)

    confidence_score: Mapped[float] = mapped_column(Float, nullable=False)

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="LOW",
    )

    root_cause: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    explanation: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    model_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    model_version: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    inference_time_ms: Mapped[Optional[float]] = mapped_column(
        Float,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    reading: Mapped["WeatherReading"] = relationship(
        "WeatherReading",
        back_populates="predictions",
    )

    alerts: Mapped[list["Alert"]] = relationship(
        "Alert",
        back_populates="prediction",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return (
            f"<Prediction id={self.id} "
            f"anomaly={self.is_anomaly} "
            f"confidence={self.confidence_score}>"
        )