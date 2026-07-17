from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models.patient_profiles import PatientProfile
from app.common.base_service import BaseService
from app.models.diagnosis import Diagnosis
from app.schemas.diagnosis import (
    DiagnosisCreate,
    DiagnosisUpdate,
)


class DiagnosisService(BaseService[Diagnosis]):

    def __init__(self):
        super().__init__(Diagnosis)

    def get_patient_diagnosis(
        self,
        db: Session,
        patient_id,
        diagnosis_id,
    ) -> Diagnosis | None:

            statement = (
                select(Diagnosis)
                .where(
                    Diagnosis.id == diagnosis_id,
                    Diagnosis.patient_id == patient_id,
                )
            )

            return db.scalar(statement)

    def create_diagnosis(
        self,
        db: Session,
        diagnosis_data: DiagnosisCreate,
        patient: PatientProfile,
    ) -> Diagnosis:

        diagnosis = Diagnosis(
            patient_id=patient.id,
            **diagnosis_data.model_dump()
        )

        return self.create(
            db,
            diagnosis,
        )

    def update_diagnosis(
        self,
        db: Session,
        diagnosis: Diagnosis,
        diagnosis_data: DiagnosisUpdate,
    ) -> Diagnosis:

        updates = diagnosis_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            diagnosis,
            updates,
        )


diagnosis_service = DiagnosisService()