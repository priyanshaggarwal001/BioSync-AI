from __future__ import annotations
import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Date, Enum, ForeignKey, String, Text, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import PrescriptionStatus
from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile
    from app.models.prescription_item import PrescriptionItem
    from app.models.hospital_record import HospitalRecord


class Prescription(Base, BaseModel):
    __tablename__ = "prescriptions"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    doctor_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    prescription_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    diagnosis: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    instructions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[PrescriptionStatus] = mapped_column(
        Enum(PrescriptionStatus),
        default=PrescriptionStatus.ACTIVE,
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    patient: Mapped["PatientProfile"] = relationship(
        back_populates="prescriptions"
    )

    items: Mapped[list["PrescriptionItem"]] = relationship(
        back_populates="prescription",
        cascade="all, delete-orphan",
    )
    hospital_record_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("hospital_records.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
    )
    hospital_record: Mapped["HospitalRecord | None"] = relationship(
    back_populates="prescriptions",
)