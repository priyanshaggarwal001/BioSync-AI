from pydantic import BaseModel, ConfigDict


class AISummaryContent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    overall_summary: str
    key_trends: list[str]
    what_this_means: str
    disclaimer: str