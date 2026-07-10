from __future__ import annotations
import uuid
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, Date, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile
    from app.models.diagnosis import Diagnosis
    from app.models.prescription import Prescription
    from app.models.lab_report import LabReport


class HospitalRecord(Base, BaseModel):
    """
    Stores imported hospital/clinic visit records.
    Serves as the source document for diagnoses,
    prescriptions, and lab reports.
    """

    __tablename__ = "hospital_records"

    patient_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    hospital_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    doctor_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    visit_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    record_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    summary: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    source_file: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    extracted_by_ai: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    extraction_status: Mapped[str] = mapped_column(
        String(20),
        default="pending",
        nullable=False,
    )

    patient_profile: Mapped["PatientProfile"] = relationship(
        back_populates="hospital_records",
    )

    diagnoses: Mapped[list["Diagnosis"]] = relationship(
    back_populates="hospital_record",
    cascade="all, delete-orphan",
    )

    prescriptions: Mapped[list["Prescription"]] = relationship(
    back_populates="hospital_record",
    cascade="all, delete-orphan",
    )

    lab_reports: Mapped[list["LabReport"]] = relationship(
    back_populates="hospital_record",
    cascade="all, delete-orphan",
    )