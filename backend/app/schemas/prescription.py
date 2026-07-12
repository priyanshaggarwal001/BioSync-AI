from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import PrescriptionStatus


class PrescriptionBase(BaseModel):
    patient_id: UUID
    doctor_name: str
    prescription_date: date
    diagnosis: str | None = None
    instructions: str | None = None
    status: PrescriptionStatus = PrescriptionStatus.ACTIVE
    notes: str | None = None
    hospital_record_id: UUID | None = None


class PrescriptionCreate(PrescriptionBase):
    pass


class PrescriptionUpdate(BaseModel):
    doctor_name: str | None = None
    prescription_date: date | None = None
    diagnosis: str | None = None
    instructions: str | None = None
    status: PrescriptionStatus | None = None
    notes: str | None = None
    hospital_record_id: UUID | None = None


class PrescriptionResponse(PrescriptionBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)