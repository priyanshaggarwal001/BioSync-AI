from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.diagnosis import Diagnosis
from app.schemas.diagnosis import (
    DiagnosisCreate,
    DiagnosisUpdate,
)


class DiagnosisService(BaseService[Diagnosis]):

    def __init__(self):
        super().__init__(Diagnosis)

    def get_by_patient_id(
        self,
        db: Session,
        patient_id,
    ) -> list[Diagnosis]:

        statement = (
            select(Diagnosis)
            .where(Diagnosis.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())

    def create_diagnosis(
        self,
        db: Session,
        diagnosis_data: DiagnosisCreate,
    ) -> Diagnosis:

        diagnosis = Diagnosis(
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