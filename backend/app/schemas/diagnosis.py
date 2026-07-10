from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DiagnosisBase(BaseModel):
    patient_id: UUID
    diagnosis_name: str
    icd10_code: str | None = None
    diagnosis_date: date | None = None
    severity: str | None = None
    status: str = "active"
    diagnosed_by: str | None = None
    source: str
    notes: str | None = None
    hospital_record_id: UUID | None = None


class DiagnosisCreate(DiagnosisBase):
    pass


class DiagnosisUpdate(BaseModel):
    diagnosis_name: str | None = None
    icd10_code: str | None = None
    diagnosis_date: date | None = None
    severity: str | None = None
    status: str | None = None
    diagnosed_by: str | None = None
    source: str | None = None
    notes: str | None = None
    hospital_record_id: UUID | None = None


class DiagnosisResponse(DiagnosisBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)