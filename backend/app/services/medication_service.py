from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.medication import Medication
from app.models.patient_profiles import PatientProfile
from app.schemas.medication import (
    MedicationCreate,
    MedicationUpdate,
)


class MedicationService(BaseService[Medication]):

    def __init__(self):
        super().__init__(Medication)

    def create_medication(
        self,
        db: Session,
        patient: PatientProfile,
        medication_data: MedicationCreate,
    ) -> Medication:

        medication = Medication(
            patient_id=patient.id,
            **medication_data.model_dump(),
        )

        return self.create(
            db,
            medication,
        )

    def get_patient_medication(
        self,
        db: Session,
        patient_id,
        medication_id,
    ) -> Medication | None:

        statement = (
            select(Medication)
            .where(
                Medication.id == medication_id,
                Medication.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_patient_medications(
        self,
        db: Session,
        patient_id,
    ) -> list[Medication]:

        statement = (
            select(Medication)
            .where(Medication.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())

    def update_medication(
        self,
        db: Session,
        medication: Medication,
        medication_data: MedicationUpdate,
    ) -> Medication:

        updates = medication_data.model_dump(
            exclude_unset=True,
        )

        return self.update(
            db,
            medication,
            updates,
        )


medication_service = MedicationService()