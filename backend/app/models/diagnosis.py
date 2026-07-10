import uuid
from datetime import date

from app.models.base_model import BaseModel
from sqlalchemy import Date, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.database.base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.hospital_record import HospitalRecord
    from app.models.patient_profiles import PatientProfile



class Diagnosis(Base,BaseModel):
    __tablename__ = "diagnoses"


    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )

    patient: Mapped["PatientProfile"] = relationship(
        back_populates="diagnoses"
    )

    diagnosis_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    icd10_code: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    diagnosis_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    severity: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="active",
    )

    diagnosed_by: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    source: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )
    hospital_record_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("hospital_records.id", ondelete="SET NULL"),
    nullable=True,
    index=True,
    )

    hospital_record: Mapped["HospitalRecord | None"] = relationship(
    back_populates="diagnoses",
    )   

    