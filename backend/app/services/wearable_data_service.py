from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.patient_profiles import PatientProfile
from app.models.wearable_data import WearableData
from app.schemas.wearable_data import (
    WearableDataCreate,
    WearableDataUpdate,
)


class WearableDataService(BaseService[WearableData]):
    def __init__(self):
        super().__init__(WearableData)

    def create_wearable_data(
        self,
        db: Session,
        patient: PatientProfile,
        wearable_data: WearableDataCreate,
    ) -> WearableData:

        wearable = WearableData(
            patient_id=patient.id,
            **wearable_data.model_dump(),
        )

        return self.create(
            db,
            wearable,
        )

    def get_patient_wearable_data(
        self,
        db: Session,
        patient_id: UUID,
        wearable_data_id: UUID,
    ) -> WearableData | None:

        statement = (
            select(WearableData)
            .where(
                WearableData.id == wearable_data_id,
                WearableData.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_patient_wearable_data_list(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[WearableData]:

        statement = (
            select(WearableData)
            .where(
                WearableData.patient_id == patient_id,
            )
        )

        return list(db.scalars(statement).all())

    def update_wearable_data(
        self,
        db: Session,
        wearable: WearableData,
        wearable_data: WearableDataUpdate,
    ) -> WearableData:

        updates = wearable_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            wearable,
            updates,
        )


wearable_data_service = WearableDataService()