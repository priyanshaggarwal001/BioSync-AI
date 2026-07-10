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

    def get_by_user_id(
        self,
        db: Session,
        user_id,
    ) -> list[ManualEntry]:

        statement = (
            select(ManualEntry)
            .where(ManualEntry.user_id == user_id)
        )

        return list(db.scalars(statement).all())

    def create_entry(
        self,
        db: Session,
        entry_data: ManualEntryCreate,
    ) -> ManualEntry:

        entry = ManualEntry(
            **entry_data.model_dump()
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