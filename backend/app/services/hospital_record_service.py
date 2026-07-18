from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.hospital_record import HospitalRecord
from app.models.patient_profiles import PatientProfile
from app.schemas.hospital_record import (
    HospitalRecordCreate,
    HospitalRecordUpdate,
)


class HospitalRecordService(BaseService[HospitalRecord]):
    def __init__(self):
        super().__init__(HospitalRecord)

    def create_hospital_record(
        self,
        db: Session,
        patient: PatientProfile,
        hospital_record_data: HospitalRecordCreate,
    ) -> HospitalRecord:

        hospital_record = HospitalRecord(
            patient_id=patient.id,
            **hospital_record_data.model_dump(),
        )

        return self.create(
            db,
            hospital_record,
        )

    def get_patient_hospital_record(
        self,
        db: Session,
        patient_id: UUID,
        record_id: UUID,
    ) -> HospitalRecord | None:

        statement = (
            select(HospitalRecord)
            .where(
                HospitalRecord.id == record_id,
                HospitalRecord.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_patient_hospital_records(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[HospitalRecord]:

        statement = (
            select(HospitalRecord)
            .where(
                HospitalRecord.patient_id == patient_id
            )
        )

        return list(db.scalars(statement).all())

    def update_hospital_record(
        self,
        db: Session,
        hospital_record: HospitalRecord,
        hospital_record_data: HospitalRecordUpdate,
    ) -> HospitalRecord:

        updates = hospital_record_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            hospital_record,
            updates,
        )


hospital_record_service = HospitalRecordService()