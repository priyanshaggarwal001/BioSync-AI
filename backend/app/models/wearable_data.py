from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel
from sqlalchemy import Enum
from app.common.enums import DataSource

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile


class WearableData(Base, BaseModel):
    """
    Stores health and fitness metrics collected from wearable devices.
    """

    __tablename__ = "wearable_data"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    source: Mapped[DataSource] = mapped_column(
    Enum(DataSource),
    nullable=False,
)

    steps: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    calories_burned: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    distance_km: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    active_minutes: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    sleep_hours: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    resting_heart_rate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    heart_rate_variability: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    vo2_max: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    stress_level: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    device_name: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    patient_profile: Mapped["PatientProfile"] = relationship(
        back_populates="wearable_data",
    )