from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class HospitalRecordBase(BaseModel):
    hospital_name: str
    doctor_name: str | None = None
    visit_date: date
    record_type: str
    summary: str | None = None
    source_file: str | None = None
    extracted_by_ai: bool = False
    extraction_status: str = "pending"


class HospitalRecordCreate(HospitalRecordBase):
    pass


class HospitalRecordUpdate(BaseModel):
    hospital_name: str | None = None
    doctor_name: str | None = None
    visit_date: date | None = None
    record_type: str | None = None
    summary: str | None = None
    source_file: str | None = None
    extracted_by_ai: bool | None = None
    extraction_status: str | None = None


class HospitalRecordResponse(HospitalRecordBase):
    id: UUID
    patient_id: UUID
    model_config = ConfigDict(from_attributes=True)