from __future__ import annotations
import uuid

from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import UUID, Date, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.common.enums import LabReportCategory, LabReportStatus
from app.database.base import Base
from app.models.base_model import BaseModel

if TYPE_CHECKING:
    from app.models.patient_profiles import PatientProfile
    from app.models.lab_report_result import LabReportResult
    from app.models.hospital_record import HospitalRecord


class LabReport(Base, BaseModel):
    __tablename__ = "lab_reports"

    patient_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("patient_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    report_name: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    category: Mapped[LabReportCategory] = mapped_column(
        Enum(LabReportCategory),
        nullable=False,
    )

    laboratory_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    doctor_name: Mapped[str | None] = mapped_column(
        String(200),
        nullable=True,
    )

    report_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    status: Mapped[LabReportStatus] = mapped_column(
        Enum(LabReportStatus),
        nullable=False,
        default=LabReportStatus.PENDING,
    )

    report_file_url: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    patient: Mapped["PatientProfile"] = relationship(
        back_populates="lab_reports"
    )

    results: Mapped[list["LabReportResult"]] = relationship(
        back_populates="lab_report",
        cascade="all, delete-orphan",
    )
    hospital_record_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("hospital_records.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    hospital_record: Mapped["HospitalRecord | None"] = relationship(
    back_populates="lab_reports",
)   