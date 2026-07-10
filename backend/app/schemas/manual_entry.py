from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class ManualEntryBase(BaseModel):
    user_id: UUID
    metric_name: str
    metric_value: Decimal
    unit: str | None = None
    category: str
    notes: str | None = None
    recorded_at: datetime


class ManualEntryCreate(ManualEntryBase):
    pass


class ManualEntryUpdate(BaseModel):
    metric_name: str | None = None
    metric_value: Decimal | None = None
    unit: str | None = None
    category: str | None = None
    notes: str | None = None
    recorded_at: datetime | None = None


class ManualEntryResponse(ManualEntryBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)