from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TimelineEvent(BaseModel):
    id: UUID
    event_type: str
    title: str
    description: str | None = None
    event_date: datetime
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(from_attributes=True)


class TimelineResponse(BaseModel):
    events: list[TimelineEvent]