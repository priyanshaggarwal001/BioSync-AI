from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.prescription_item import PrescriptionItem
from app.schemas.prescription_item import (
    PrescriptionItemCreate,
    PrescriptionItemResponse,
    PrescriptionItemUpdate,
)
from app.services.prescription_item_service import (
    prescription_item_service,
)

router = APIRouter(
    prefix="/prescription-items",
    tags=["Prescription Items"],
)


@router.post("/", response_model=PrescriptionItemResponse)
def create_prescription_item(
    prescription_item: PrescriptionItemCreate,
    db: Session = Depends(get_db),
):
    item = PrescriptionItem(**prescription_item.model_dump())
    return prescription_item_service.create(db, item)


@router.get("/", response_model=list[PrescriptionItemResponse])
def get_prescription_items(
    db: Session = Depends(get_db),
):
    return prescription_item_service.get_all(db)


@router.get("/{item_id}", response_model=PrescriptionItemResponse)
def get_prescription_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    return prescription_item_service.get_by_id(db, item_id)


@router.put("/{item_id}", response_model=PrescriptionItemResponse)
def update_prescription_item(
    item_id: UUID,
    prescription_item: PrescriptionItemUpdate,
    db: Session = Depends(get_db),
):
    return prescription_item_service.update(
        db,
        item_id,
        prescription_item.model_dump(exclude_unset=True),
    )


@router.delete("/{item_id}")
def delete_prescription_item(
    item_id: UUID,
    db: Session = Depends(get_db),
):
    prescription_item_service.delete(db, item_id)
    return {
        "message": "Prescription item deleted successfully"
    }