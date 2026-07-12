from __future__ import annotations

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import DataSource


class WearableDataBase(BaseModel):
    patient_profile_id: UUID
    recorded_at: datetime
    source: DataSource
    steps: int | None = None
    calories_burned: float | None = None
    distance_km: float | None = None
    active_minutes: int | None = None
    sleep_hours: float | None = None
    resting_heart_rate: float | None = None
    heart_rate_variability: float | None = None
    vo2_max: float | None = None
    stress_level: float | None = None
    device_name: str | None = None
    notes: str | None = None


class WearableDataCreate(WearableDataBase):
    pass


class WearableDataUpdate(BaseModel):
    recorded_at: datetime | None = None
    source: DataSource | None = None
    steps: int | None = None
    calories_burned: float | None = None
    distance_km: float | None = None
    active_minutes: int | None = None
    sleep_hours: float | None = None
    resting_heart_rate: float | None = None
    heart_rate_variability: float | None = None
    vo2_max: float | None = None
    stress_level: float | None = None
    device_name: str | None = None
    notes: str | None = None


class WearableDataResponse(WearableDataBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)