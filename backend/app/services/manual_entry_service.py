from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.manual_entry import ManualEntry
from app.schemas.manual_entry import (
    ManualEntryCreate,
    ManualEntryUpdate,
)


class ManualEntryService(BaseService[ManualEntry]):

    def __init__(self):
        super().__init__(ManualEntry)

    def get_user_entries(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[ManualEntry]:

        statement = (
            select(ManualEntry)
            .where(ManualEntry.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())

    def get_user_entry(
        self,
        db: Session,
        patient_id: UUID,
        entry_id: UUID,
    ) -> ManualEntry | None:

        statement = (
            select(ManualEntry)
            .where(
                ManualEntry.id == entry_id,
                ManualEntry.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def create_entry(
        self,
        db: Session,
        patient_id: UUID,
        entry_data: ManualEntryCreate,
    ) -> ManualEntry:

        entry = ManualEntry(
            patient_id=patient_id,
            **entry_data.model_dump(),
        )

        return self.create(
            db,
            entry,
        )

    def update_entry(
        self,
        db: Session,
        entry: ManualEntry,
        entry_data: ManualEntryUpdate,
    ) -> ManualEntry:

        updates = entry_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            entry,
            updates,
        )


manual_entry_service = ManualEntryService()