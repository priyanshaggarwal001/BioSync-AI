from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class DashboardResponse(BaseModel):
    patient_id: UUID
    patient_name: str

    wellness_score: int
    wellness_score_status: str

    latest_vital: dict[str, Any] | None = None
    latest_wearable: dict[str, Any] | None = None

    active_medications: int
    recent_diagnoses: int

    recent_events: list[dict[str, Any]]
    insights: list[dict[str, Any]]

    model_config = ConfigDict(from_attributes=True)