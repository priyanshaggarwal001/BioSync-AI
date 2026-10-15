
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class GuidanceItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    metric: str
    category: str
    observation: str
    suggestion: str
    priority: Literal["general"]
    ai_explanation: str | None = None


class AIGuidanceResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: Literal[
        "guidance_available",
        "no_guidance_triggered",
        "insufficient_data",
    ]

    guidance: list[GuidanceItem] = Field(default_factory=list)
    message: str
    ai_model: str | None = None
    ai_explanation_status: Literal[
        "generated",
        "fallback",
    ] | None = None
