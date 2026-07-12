from datetime import date, datetime
from uuid import UUID
from app.common.enums import (
    DiagnosisStatus,
    SeverityLevel,
    RecordSource,
)

from pydantic import BaseModel, ConfigDict


class DiagnosisBase(BaseModel):
    patient_id: UUID
    diagnosis_name: str
    icd10_code: str | None = None
    diagnosis_date: date | None = None
    severity: SeverityLevel | None = None
    status: DiagnosisStatus = DiagnosisStatus.ACTIVE
    diagnosed_by: str | None = None
    source: RecordSource
    notes: str | None = None
    hospital_record_id: UUID | None = None


class DiagnosisCreate(DiagnosisBase):
    pass


class DiagnosisUpdate(BaseModel):
    diagnosis_name: str | None = None
    icd10_code: str | None = None
    diagnosis_date: date | None = None
    severity: SeverityLevel | None = None
    status: DiagnosisStatus | None = None
    diagnosed_by: str | None = None
    source: RecordSource | None = None
    notes: str | None = None
    hospital_record_id: UUID | None = None


class DiagnosisResponse(DiagnosisBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)