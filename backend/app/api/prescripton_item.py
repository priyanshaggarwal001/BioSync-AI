from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
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


@router.post(
    "/",
    response_model=PrescriptionItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prescription_item(
    item_data: PrescriptionItemCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    try:
        return prescription_item_service.create_prescription_item(
            db,
            patient,
            item_data,
            
            
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )


@router.get(
    "/",
    response_model=list[PrescriptionItemResponse],
)
def get_prescription_items(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return prescription_item_service.get_prescription_items(
        db,
        patient.id,
    )


@router.get(
    "/{item_id}",
    response_model=PrescriptionItemResponse,
)
def get_prescription_item(
    item_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    item = prescription_item_service.get_prescription_item(
        db,
        patient.id,
        item_id,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription item not found.",
        )

    return item


@router.put(
    "/{item_id}",
    response_model=PrescriptionItemResponse,
)
def update_prescription_item(
    item_id: UUID,
    item_data: PrescriptionItemUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    item = prescription_item_service.get_prescription_item(
        db,
        patient.id,
        item_id,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription item not found.",
        )

    return prescription_item_service.update_prescription_item(
        db,
        item,
        item_data,
    )


@router.delete(
    "/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_prescription_item(
    item_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    item = prescription_item_service.get_prescription_item(
        db,
        patient.id,
        item_id,
    )

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription item not found.",
        )

    prescription_item_service.delete(
        db,
        item,
    )