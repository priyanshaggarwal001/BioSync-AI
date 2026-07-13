from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.common.enums import BloodGroup, Gender


class PatientProfileBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: Gender
    blood_group: BloodGroup
    phone_number: str
    height_cm: Decimal
    weight_kg: Decimal
    emergency_contact_name: str
    emergency_contact_phone: str


class PatientProfileCreate(PatientProfileBase):
    pass


class PatientProfileUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    date_of_birth: date | None = None
    gender: Gender | None = None
    blood_group: BloodGroup | None = None
    phone_number: str | None = None
    height_cm: Decimal | None = None
    weight_kg: Decimal | None = None
    emergency_contact_name: str | None = None
    emergency_contact_phone: str | None = None
    

class PatientProfileResponse(PatientProfileBase):
    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)