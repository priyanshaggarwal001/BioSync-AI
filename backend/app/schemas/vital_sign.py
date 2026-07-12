from __future__ import annotations
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class VitalSignBase(BaseModel):
    patient_profile_id: UUID
    recorded_at: datetime
    source: str
    systolic_bp: float | None = None
    diastolic_bp: float | None = None
    heart_rate: float | None = None
    respiratory_rate: float | None = None
    body_temperature: float | None = None
    oxygen_saturation: float | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    bmi: float | None = None
    device_name: str | None = None
    notes: str | None = None

class VitalSignCreate(VitalSignBase):
    pass

class VitalSignUpdate(BaseModel):
    recorded_at: datetime | None = None
    source: str | None = None
    systolic_bp: float | None = None
    diastolic_bp: float | None = None
    heart_rate: float | None = None
    respiratory_rate: float | None = None
    body_temperature: float | None = None
    oxygen_saturation: float | None = None
    height_cm: float | None = None
    weight_kg: float | None = None
    bmi: float | None = None
    device_name: str | None = None
    notes: str | None = None

class VitalSignResponse(VitalSignBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)
