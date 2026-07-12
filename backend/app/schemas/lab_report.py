from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import (
    LabReportCategory,
    LabReportStatus,
)


class LabReportBase(BaseModel):
    patient_id: UUID
    report_name: str
    category: LabReportCategory
    laboratory_name: str | None = None
    doctor_name: str | None = None
    report_date: date
    status: LabReportStatus = LabReportStatus.PENDING
    report_file_url: str | None = None
    notes: str | None = None
    hospital_record_id: UUID | None = None


class LabReportCreate(LabReportBase):
    pass


class LabReportUpdate(BaseModel):
    report_name: str | None = None
    category: LabReportCategory | None = None
    laboratory_name: str | None = None
    doctor_name: str | None = None
    report_date: date | None = None
    status: LabReportStatus | None = None
    report_file_url: str | None = None
    notes: str | None = None
    hospital_record_id: UUID | None = None


class LabReportResponse(LabReportBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)