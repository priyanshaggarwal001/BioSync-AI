from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.patient_profiles import PatientProfile
from app.models.prescription import Prescription
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate,
)


class PrescriptionService(BaseService[Prescription]):
    def __init__(self):
        super().__init__(Prescription)

    def create_prescription(
        self,
        db: Session,
        patient: PatientProfile,
        prescription_data: PrescriptionCreate,
    ) -> Prescription:

        prescription = Prescription(
            patient_id=patient.id,
            **prescription_data.model_dump(),
        )

        return self.create(
            db,
            prescription,
        )

    def get_patient_prescription(
        self,
        db: Session,
        patient_id: UUID,
        prescription_id: UUID,
    ) -> Prescription | None:

        statement = (
            select(Prescription)
            .where(
                Prescription.id == prescription_id,
                Prescription.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_patient_prescriptions(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[Prescription]:

        statement = (
            select(Prescription)
            .where(Prescription.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())

    def update_prescription(
        self,
        db: Session,
        prescription: Prescription,
        prescription_data: PrescriptionUpdate,
    ) -> Prescription:

        updates = prescription_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            prescription,
            updates,
        )


prescription_service = PrescriptionService()