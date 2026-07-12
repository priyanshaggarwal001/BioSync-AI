from __future__ import annotations

from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import LabResultStatus


class LabReportResultBase(BaseModel):
    lab_report_id: UUID
    parameter_name: str
    parameter_value: str
    unit: str | None = None
    reference_range: str | None = None
    status: LabResultStatus


class LabReportResultCreate(LabReportResultBase):
    pass


class LabReportResultUpdate(BaseModel):
    parameter_name: str | None = None
    parameter_value: str | None = None
    unit: str | None = None
    reference_range: str | None = None
    status: LabResultStatus | None = None


class LabReportResultResponse(LabReportResultBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)