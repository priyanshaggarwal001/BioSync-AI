from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.medication import Medication
from app.schemas.medication import (
    MedicationCreate,
    MedicationResponse,
    MedicationUpdate,
)
from app.services.medication_service import medication_service

router = APIRouter(prefix="/medications", tags=["Medications"])


@router.post("/", response_model=MedicationResponse)
def create_medication(
    medication: MedicationCreate,
    db: Session = Depends(get_db),
):
    medication_obj = Medication(**medication.model_dump())
    return medication_service.create(db, medication_obj)


@router.get("/", response_model=list[MedicationResponse])
def get_medications(db: Session = Depends(get_db)):
    return medication_service.get_all(db)


@router.get("/{medication_id}", response_model=MedicationResponse)
def get_medication(
    medication_id: UUID,
    db: Session = Depends(get_db),
):
    return medication_service.get_by_id(db, medication_id)


@router.put("/{medication_id}", response_model=MedicationResponse)
def update_medication(
    medication_id: UUID,
    medication: MedicationUpdate,
    db: Session = Depends(get_db),
):
    return medication_service.update(
        db,
        medication_id,
        medication.model_dump(exclude_unset=True),
    )


@router.delete("/{medication_id}")
def delete_medication(
    medication_id: UUID,
    db: Session = Depends(get_db),
):
    medication_service.delete(db, medication_id)
    return {"message": "Medication deleted successfully"}