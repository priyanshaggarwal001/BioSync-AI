from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile


class VitalSign(Base, BaseModel):
    """
    Stores a patient's vital sign measurements.
    """

    __tablename__ = "vital_signs"

    patient_profile_id: Mapped[str] = mapped_column(
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    recorded_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    systolic_bp: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    diastolic_bp: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    heart_rate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    respiratory_rate: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    body_temperature: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    oxygen_saturation: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    height_cm: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    weight_kg: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    bmi: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )
    device_name: Mapped[str | None] = mapped_column(
    String(100),
    nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
    String(500),
    nullable=True,
    )

    patient_profile: Mapped["PatientProfile"] = relationship(
        back_populates="vital_signs",
    )