from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.allergy import Allergy
from app.schemas.allergy import AllergyCreate, AllergyUpdate


class AllergyService(BaseService[Allergy]):
    def __init__(self):
        super().__init__(Allergy)

    def create_allergy(
        self,
        db: Session,
        allergy_data: AllergyCreate,
    ) -> Allergy:
        allergy = Allergy(**allergy_data.model_dump())

        return self.create(
            db,
            allergy,
        )

    def update_allergy(
        self,
        db: Session,
        allergy: Allergy,
        allergy_data: AllergyUpdate,
    ) -> Allergy:
        update_data = allergy_data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(
                allergy,
                field,
                value,
            )

        db.commit()
        db.refresh(allergy)

        return allergy


allergy_service = AllergyService()