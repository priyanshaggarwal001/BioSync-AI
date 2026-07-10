from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING
import uuid
from sqlalchemy import Boolean, Date, Enum, ForeignKey, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import (
    MedicationDosageForm,
    MedicationFrequency,
    MedicationRoute,
)
from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile
    from app.models.prescription_item import PrescriptionItem


class Medication(Base, BaseModel):
    __tablename__ = "medications"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    medication_name: Mapped[str] = mapped_column(String(150), nullable=False)

    generic_name: Mapped[str | None] = mapped_column(String(150))

    brand_name: Mapped[str | None] = mapped_column(String(150))

    dosage: Mapped[str] = mapped_column(String(50), nullable=False)

    dosage_form: Mapped[MedicationDosageForm] = mapped_column(
        Enum(MedicationDosageForm),
        nullable=False,
    )

    route: Mapped[MedicationRoute] = mapped_column(
        Enum(MedicationRoute),
        nullable=False,
    )

    frequency: Mapped[MedicationFrequency] = mapped_column(
        Enum(MedicationFrequency),
        nullable=False,
    )

    indication: Mapped[str | None] = mapped_column(Text)

    start_date: Mapped[date] = mapped_column(Date)

    end_date: Mapped[date | None] = mapped_column(Date)

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(Text)

    # Relationships

    patient: Mapped["PatientProfile"] = relationship(
        back_populates="medications"
    )

    prescription_items: Mapped[list["PrescriptionItem"]] = relationship(
        back_populates="medication"
    )