from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.patient_profiles import PatientProfile
from app.models.prescription import Prescription
from app.models.prescription_item import PrescriptionItem
from app.schemas.prescription_item import (
    PrescriptionItemCreate,
    PrescriptionItemUpdate,
)


class PrescriptionItemService(BaseService[PrescriptionItem]):
    def __init__(self):
        super().__init__(PrescriptionItem)

    def create_prescription_item(
        self,
        db: Session,
        patient: PatientProfile,
        item_data: PrescriptionItemCreate,
    ) -> PrescriptionItem:

        prescription = db.scalar(
            select(Prescription).where(
                Prescription.id == item_data.prescription_id,
                Prescription.patient_id == patient.id,
            )
        )

        if not prescription:
            raise ValueError("Prescription not found.")

        item = PrescriptionItem(
            **item_data.model_dump(),
        )

        return self.create(db, item)

    def get_prescription_item(
        self,
        db: Session,
        patient_id: UUID,
        item_id: UUID,
    ) -> PrescriptionItem | None:

        statement = (
            select(PrescriptionItem)
            .join(Prescription)
            .where(
                PrescriptionItem.id == item_id,
                Prescription.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_prescription_items(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[PrescriptionItem]:

        statement = (
            select(PrescriptionItem)
            .join(Prescription)
            .where(
                Prescription.patient_id == patient_id,
            )
        )

        return list(db.scalars(statement).all())

    def update_prescription_item(
        self,
        db: Session,
        item: PrescriptionItem,
        item_data: PrescriptionItemUpdate,
    ) -> PrescriptionItem:

        updates = item_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            item,
            updates,
        )


prescription_item_service = PrescriptionItemService()