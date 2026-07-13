from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.patient_profiles import PatientProfile
from app.common.base_service import BaseService
from app.models.allergy import Allergy
from app.schemas.allergy import AllergyCreate, AllergyUpdate


class AllergyService(BaseService[Allergy]):
    def __init__(self):
        super().__init__(Allergy)

    def create_allergy(
        self,
        db: Session,
        patient: PatientProfile,
        allergy_data: AllergyCreate,
    ) -> Allergy:

        allergy = Allergy(
            patient_id=patient.id,
            **allergy_data.model_dump(),
        )

        return self.create(
            db,
            allergy,
        )

    def update_allergy(
        self,
        db: Session,
        allergy: Allergy,
        allergy_data: AllergyUpdate,
    ) -> Allergy:
        update_data = allergy_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(
                allergy,
                field,
                value,
            )

        db.commit()
        db.refresh(allergy)

        return allergy
    def get_patient_allergy(
        self,
        db: Session,
        patient_id,
        allergy_id,
    ) -> Allergy | None:

        statement = (
            select(Allergy)
            .where(
                Allergy.id == allergy_id,
                Allergy.patient_id == patient_id,
            )
        )

        return db.scalar(statement)
    def get_patient_allergies(
        self,
        db: Session,
        patient_id,
    ) -> list[Allergy]:

        statement = (
            select(Allergy)
            .where(Allergy.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())


allergy_service = AllergyService()
