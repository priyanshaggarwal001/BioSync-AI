from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.prescription import Prescription
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse,
    PrescriptionUpdate,
)
from app.services.prescription_service import prescription_service

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"],
)


@router.post("/", response_model=PrescriptionResponse)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
):
    prescription_obj = Prescription(**prescription.model_dump())
    return prescription_service.create(db, prescription_obj)


@router.get("/", response_model=list[PrescriptionResponse])
def get_prescriptions(
    db: Session = Depends(get_db),
):
    return prescription_service.get_all(db)


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription(
    prescription_id: UUID,
    db: Session = Depends(get_db),
):
    return prescription_service.get_by_id(
        db,
        prescription_id,
    )


@router.put("/{prescription_id}", response_model=PrescriptionResponse)
def update_prescription(
    prescription_id: UUID,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db),
):
    return prescription_service.update(
        db,
        prescription_id,
        prescription.model_dump(exclude_unset=True),
    )


@router.delete("/{prescription_id}")
def delete_prescription(
    prescription_id: UUID,
    db: Session = Depends(get_db),
):
    prescription_service.delete(
        db,
        prescription_id,
    )
    return {
        "message": "Prescription deleted successfully"
    }