# ---------------------------------------------------------------------------
# app/models/weather_reading.py
#
# ORM model for the "weather_readings" table — a single sensor reading
# taken at a station at a specific point in time. Many readings belong to
# one station (many-to-one from this model's perspective).
# ---------------------------------------------------------------------------

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

# TYPE_CHECKING-only import: lets type checkers/IDEs resolve the "Station"
# type hint below without creating a real circular import at runtime
# (weather_reading.py and station.py both reference each other's classes,
# but neither needs to actually import the other's module at import time —
# relationship() resolves the "Station" string lazily, later).
if TYPE_CHECKING:
    from app.models.station import Station
    from app.models.prediction import Prediction


class WeatherReading(Base):
    """A single weather sensor reading recorded at a station."""

    __tablename__ = "weather_readings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Foreign key linking this reading to its parent station.
    # ondelete="CASCADE" is a DATABASE-level instruction: if the parent
    # station row is deleted directly in PostgreSQL (not just through
    # SQLAlchemy), the DB itself deletes dependent readings too, keeping
    # this in sync with the ORM-level cascade on the Station side.
    # index=True speeds up the very common query "all readings for
    # station X".
    station_id: Mapped[int] = mapped_column(
        ForeignKey("stations.id", ondelete="CASCADE"), nullable=False, index=True
    )

    # Sensor measurements for this reading.
    temperature: Mapped[float] = mapped_column(Float, nullable=False)
    pressure: Mapped[float] = mapped_column(Float, nullable=False)
    humidity: Mapped[float] = mapped_column(Float, nullable=False)

    # When the reading was actually taken (not when the row was inserted).
    # Indexed because time-range queries ("readings from the last 24h")
    # will be one of the most frequent access patterns on this table.
    recorded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, index=True)

    # ORM-level relationship back to the parent Station. back_populates
    # keeps both sides (Station.weather_readings and this .station) in
    # sync automatically whenever one side is set in Python.
    station: Mapped["Station"] = relationship("Station", back_populates="weather_readings")

    # Predictions associated with this reading
    predictions: Mapped[list["Prediction"]] = relationship(
        "Prediction",
        back_populates="reading",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<WeatherReading id={self.id} station_id={self.station_id} recorded_at={self.recorded_at.isoformat()}>"