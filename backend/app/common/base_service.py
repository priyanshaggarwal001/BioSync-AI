from typing import Any, Generic, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")


class BaseService(Generic[ModelType]):
    """
    Generic CRUD service.
    Every service in the project inherits from this class.
    """

    model: type[ModelType]

    def __init__(self, model: type[ModelType]):
        self.model = model

    def create(
        self,
        db: Session,
        obj: ModelType,
    ) -> ModelType:
        try:
            db.add(obj)
            db.commit()
            db.refresh(obj)
            return obj

        except Exception:
            db.rollback()
            raise

    def get_by_id(
        self,
        db: Session,
        object_id: Any,
    ) -> ModelType | None:

        return db.get(self.model, object_id)

    def get_all(
        self,
        db: Session,
    ) -> list[ModelType]:

        statement = select(self.model)

        return list(db.scalars(statement).all())

    def update(
        self,
        db: Session,
        obj: ModelType,
        updates: dict,
    ) -> ModelType:

        for key, value in updates.items():
             if hasattr(obj, key):
                setattr(obj, key, value)

        db.commit()
        db.refresh(obj)

        return obj

    def delete(
        self,
        db: Session,
        obj: ModelType,
    ) -> None:

        db.delete(obj)
        db.commit()