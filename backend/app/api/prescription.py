from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.prescription import (
    PrescriptionCreate,
    PrescriptionResponse,
    PrescriptionUpdate,
)
from app.services.prescription_service import (
    prescription_service,
)

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"],
)


@router.post(
    "/",
    response_model=PrescriptionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_prescription(
    prescription_data: PrescriptionCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return prescription_service.create_prescription(
        db,
        patient,
        prescription_data,
        
        
    )


@router.get(
    "/",
    response_model=list[PrescriptionResponse],
)
def get_prescriptions(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return prescription_service.get_patient_prescriptions(
        db,
        patient.id,
    )


@router.get(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
)
def get_prescription(
    prescription_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    prescription = prescription_service.get_patient_prescription(
        db,
        patient.id,
        prescription_id,
    )

    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found.",
        )

    return prescription


@router.put(
    "/{prescription_id}",
    response_model=PrescriptionResponse,
)
def update_prescription(
    prescription_id: UUID,
    prescription_data: PrescriptionUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    prescription = prescription_service.get_patient_prescription(
        db,
        patient.id,
        prescription_id,
    )

    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found.",
        )

    return prescription_service.update_prescription(
        db,
        prescription,
        prescription_data,
    )


@router.delete(
    "/{prescription_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_prescription(
    prescription_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    prescription = prescription_service.get_patient_prescription(
        db,
        patient.id,
        prescription_id,
    )

    if not prescription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Prescription not found.",
        )

    prescription_service.delete(
        db,
        prescription,
    )