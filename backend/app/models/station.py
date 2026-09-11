# ---------------------------------------------------------------------------
# app/models/station.py
#
# ORM model for the "stations" table — represents a single physical
# monitoring station. Written in SQLAlchemy 2.x style using Mapped /
# mapped_column, which gives full static typing support (mypy/IDE
# autocomplete) instead of the older Column(...) style.
#
# No relationships to other tables are defined yet, as requested.
# ---------------------------------------------------------------------------

from datetime import date
from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.weather_reading import WeatherReading


class Station(Base):
    """A physical monitoring station tracked by SkyGuard AI."""

    # The actual PostgreSQL table name this class maps to.
    __tablename__ = "stations"

    # Primary key. `index=True` is redundant with primary_key (PKs are
    # automatically indexed), but included since it was explicitly
    # requested — harmless and sometimes kept for clarity/consistency.
    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    # Unique short code identifying the station (e.g. "STN-001").
    # unique=True enforces no two stations share a code at the DB level.
    # index=True speeds up lookups by code, which will be a common query.
    station_code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)

    # Human-readable station name.
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Location fields — kept as plain strings for now (no separate
    # City/State tables), since relationships aren't in scope yet.
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)

    # Geographic coordinates, required for any mapping/proximity features.
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)

    # Operational status of the station. Kept as a plain String (not an
    # Enum) for now to keep this a pure foundation model; a DB-level
    # CHECK constraint or Enum type can be added later once the set of
    # valid statuses is finalized.
    status: Mapped[str] = mapped_column(String(20), default="ACTIVE", nullable=False)

    # Date the station was installed. Required — every station must have one.
    installation_date: Mapped[date] = mapped_column(Date, nullable=False)

    # Date of the most recent maintenance visit. Optional because a
    # newly installed station may not have been serviced yet.
    last_maintenance: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # All sensor readings collected by this station
    weather_readings: Mapped[list["WeatherReading"]] = relationship(
        "WeatherReading",
        back_populates="station",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        # Developer-friendly representation, useful in logs/debuggers —
        # never used by SQLAlchemy internals or the API layer.
        return f"<Station id={self.id} code={self.station_code!r} status={self.status!r}>"