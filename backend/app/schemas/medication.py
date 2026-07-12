from __future__ import annotations

from datetime import date
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import (
    MedicationDosageForm,
    MedicationFrequency,
    MedicationRoute,
)


class MedicationBase(BaseModel):
    patient_id: UUID
    medication_name: str
    generic_name: str | None = None
    brand_name: str | None = None
    dosage: str
    dosage_form: MedicationDosageForm
    route: MedicationRoute
    frequency: MedicationFrequency
    indication: str | None = None
    start_date: date
    end_date: date | None = None
    is_active: bool = True
    notes: str | None = None


class MedicationCreate(MedicationBase):
    pass


class MedicationUpdate(BaseModel):
    medication_name: str | None = None
    generic_name: str | None = None
    brand_name: str |None = None
    dosage: str | None = None
    dosage_form: MedicationDosageForm | None = None
    route: MedicationRoute | None = None
    frequency: MedicationFrequency | None = None
    indication: str | None = None
    start_date: date | None = None
    end_date: date | None = None
    is_active: bool | None = None
    notes: str | None = None


class MedicationResponse(MedicationBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)