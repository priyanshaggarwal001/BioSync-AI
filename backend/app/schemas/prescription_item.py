from __future__ import annotations
from datetime import datetime

from uuid import UUID

from pydantic import BaseModel, ConfigDict


class PrescriptionItemBase(BaseModel):
    prescription_id: UUID
    medication_id: UUID
    quantity: int
    duration_days: int
    morning: bool = False
    afternoon: bool = False
    evening: bool = False
    night: bool = False
    before_food: bool = False
    after_food: bool = False
    remarks: str | None = None


class PrescriptionItemCreate(PrescriptionItemBase):
    pass


class PrescriptionItemUpdate(BaseModel):
    quantity: int | None = None
    duration_days: int | None = None
    morning: bool | None = None
    afternoon: bool | None = None
    evening: bool | None = None
    night: bool | None = None
    before_food: bool | None = None
    after_food: bool | None = None
    remarks: str | None = None


class PrescriptionItemResponse(PrescriptionItemBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)