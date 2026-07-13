from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.user import User
from app.common.base_service import BaseService
from app.models.patient_profiles import PatientProfile
from app.schemas.patient_profile import (
    PatientProfileCreate,
    PatientProfileUpdate,
)


class PatientProfileService(BaseService[PatientProfile]):

    def __init__(self):
        super().__init__(PatientProfile)

    def get_by_user_id(
        self,
        db: Session,
        user_id,
    ) -> PatientProfile | None:

        statement = (
            select(PatientProfile)
            .where(PatientProfile.user_id == user_id)
        )

        return db.scalar(statement)

    def create_profile(
        self,
        db: Session,
        user: User,
        profile_data: PatientProfileCreate,
    ) -> PatientProfile:

        profile = PatientProfile(
            user_id=user.id,
            **profile_data.model_dump(),
        )

        return self.create(
            db,
            profile,
        )

    def update_profile(
        self,
        db: Session,
        profile: PatientProfile,
        profile_data: PatientProfileUpdate,
    ) -> PatientProfile:

        updates = profile_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            profile,
            updates,
        )


patient_profile_service = PatientProfileService()