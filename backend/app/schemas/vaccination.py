from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class VaccinationBase(BaseModel):
    vaccine_name: str
    manufacturer: str | None = None
    dose_number: int | None = None
    administered_date: date
    administered_by: str | None = None
    batch_number: str | None = None
    next_due_date: date | None = None
    status: str = "completed"
    notes: str | None = None


class VaccinationCreate(VaccinationBase):
    pass


class VaccinationUpdate(BaseModel):
    vaccine_name: str | None = None
    manufacturer: str | None = None
    dose_number: int | None = None
    administered_date: date | None = None
    administered_by: str | None = None
    batch_number: str | None = None
    next_due_date: date | None = None
    status: str | None = None
    notes: str | None = None


class VaccinationResponse(VaccinationBase):
    id: UUID
    patient_id: UUID
    model_config = ConfigDict(from_attributes=True)