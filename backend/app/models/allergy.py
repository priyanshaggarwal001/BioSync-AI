from __future__ import annotations

import uuid
from sqlalchemy.dialects.postgresql import UUID
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel
from app.common.enums import AllergyType, AllergySeverity

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile






class Allergy(Base, BaseModel):
    __tablename__ = "allergies"

    patient_id: Mapped[uuid.UUID] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("patient_profiles.id", ondelete="CASCADE"),
    nullable=False,
    index=True,
    )

    allergy_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    allergy_type: Mapped[AllergyType] = mapped_column(
        Enum(AllergyType),
        nullable=False,
    )

    severity: Mapped[AllergySeverity] = mapped_column(
        Enum(AllergySeverity),
        nullable=False,
    )

    reaction: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    diagnosed_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    patient: Mapped["PatientProfile"] = relationship(
        back_populates="allergies"
    )