from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.patient_profiles import PatientProfile
from app.models.vaccination import Vaccination
from app.schemas.vaccination import (
    VaccinationCreate,
    VaccinationUpdate,
)


class VaccinationService(BaseService[Vaccination]):
    def __init__(self):
        super().__init__(Vaccination)

    def create_vaccination(
        self,
        db: Session,
        patient: PatientProfile,
        vaccination_data: VaccinationCreate,
    ) -> Vaccination:

        vaccination = Vaccination(
            patient_id=patient.id,
            **vaccination_data.model_dump(),
        )

        return self.create(
            db,
            vaccination,
        )

    def update_vaccination(
        self,
        db: Session,
        vaccination: Vaccination,
        vaccination_data: VaccinationUpdate,
    ) -> Vaccination:

        return self.update(
            db,
            vaccination,
            vaccination_data.model_dump(exclude_unset=True),
        )

    def get_patient_vaccination(
        self,
        db: Session,
        patient_id,
        vaccination_id,
    ) -> Vaccination | None:

        statement = (
            select(Vaccination)
            .where(
                Vaccination.id == vaccination_id,
                Vaccination.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_patient_vaccinations(
        self,
        db: Session,
        patient_id,
    ) -> list[Vaccination]:

        statement = (
            select(Vaccination)
            .where(Vaccination.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())


vaccination_service = VaccinationService()