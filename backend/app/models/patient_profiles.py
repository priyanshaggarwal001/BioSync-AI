from __future__ import annotations


import uuid
from datetime import date

from sqlalchemy import (
    Date,
    Enum,
    ForeignKey,
    Numeric,
    String,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base
from app.models.base_model import BaseModel

from app.common.enums import Gender, BloodGroup
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.allergy import Allergy
    from app.models.lab_report import LabReport
    from app.models.medication import Medication
    from app.models.diagnosis import Diagnosis
    from app.models.user import User
    from app.models.prescription import Prescription
    from app.models.hospital_record import HospitalRecord
    from app.models.vital_sign import VitalSign
    from app.models.wearable_data import WearableData
    from app.models.vaccination import Vaccination

class PatientProfile(Base, BaseModel):
    """
    Stores patient demographic information.
    """

    __tablename__ = "patient_profiles"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    first_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    last_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    date_of_birth: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    gender: Mapped[Gender] = mapped_column(
        Enum(Gender),
        nullable=False,
    )

    blood_group: Mapped[BloodGroup] = mapped_column(
        Enum(BloodGroup),
        nullable=False,
    )

    phone_number: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    height_cm: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    weight_kg: Mapped[float] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    emergency_contact_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    emergency_contact_phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="patient_profile"
    )

    diagnoses: Mapped[list["Diagnosis"]] = relationship(
    back_populates="patient",
    cascade="all, delete-orphan",
    )
    allergies: Mapped[list["Allergy"]] = relationship(
    back_populates="patient",
    cascade="all, delete-orphan",
    )
    lab_reports: Mapped[list["LabReport"]] = relationship(
    back_populates="patient",
    cascade="all, delete-orphan",
    )
    medications: Mapped[list["Medication"]] = relationship(
    back_populates="patient",
    cascade="all, delete-orphan",
    )

    prescriptions: Mapped[list["Prescription"]] = relationship(
    back_populates="patient",
    cascade="all, delete-orphan",
    )

    hospital_records: Mapped[list["HospitalRecord"]] = relationship(
    back_populates="patient_profile",
    cascade="all, delete-orphan",
    )   
    vital_signs: Mapped[list["VitalSign"]] = relationship(
    back_populates="patient_profile",
    cascade="all, delete-orphan",
    )
    wearable_data: Mapped[list["WearableData"]] = relationship(
    back_populates="patient_profile",
    cascade="all, delete-orphan",
    )
    vaccinations: Mapped[list["Vaccination"]] = relationship(
    back_populates="patient_profile",
    cascade="all, delete-orphan",
)