from __future__ import annotations
import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Integer, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile


class Vaccination(Base, BaseModel):
    """
    Stores a patient's vaccination history.
    """

    __tablename__ = "vaccinations"

    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    vaccine_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    manufacturer: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    dose_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    administered_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    administered_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    batch_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    next_due_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="completed",
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    patient_profile: Mapped["PatientProfile"] = relationship(
        back_populates="vaccinations",
    )