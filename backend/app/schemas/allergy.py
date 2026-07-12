from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import AllergySeverity, AllergyType


class AllergyBase(BaseModel):
    patient_id: UUID
    allergy_name: str
    allergy_type: AllergyType
    severity: AllergySeverity
    reaction: str | None = None
    diagnosed_date: date | None = None
    is_active: bool = True
    notes: str | None = None


class AllergyCreate(AllergyBase):
    pass


class AllergyUpdate(BaseModel):
    allergy_name: str | None = None
    allergy_type: AllergyType | None = None
    severity: AllergySeverity | None = None
    reaction: str | None = None
    diagnosed_date: date | None = None
    is_active: bool | None = None
    notes: str | None = None


class AllergyResponse(AllergyBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)