from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.prediction import Prediction


class Alert(Base):
    """Alert generated when an anomaly is detected."""

    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    prediction_id: Mapped[int] = mapped_column(
        ForeignKey("predictions.id"),
        nullable=False,
        index=True,
    )

    alert_status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
        nullable=False,
    )

    assigned_engineer: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
    )

    resolution_notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    resolved_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        nullable=True,
    )

    prediction: Mapped["Prediction"] = relationship(
        "Prediction",
        back_populates="alerts",
    )

    def __repr__(self):
        return f"<Alert id={self.id} status={self.alert_status}>"