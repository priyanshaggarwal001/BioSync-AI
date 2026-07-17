from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.medication import (
    MedicationCreate,
    MedicationResponse,
    MedicationUpdate,
)
from app.services.medication_service import medication_service

router = APIRouter(
    prefix="/medications",
    tags=["Medications"],
)


@router.post(
    "/",
    response_model=MedicationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_medication(
    medication_data: MedicationCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return medication_service.create_medication(
        db,
        patient,
        medication_data,
    )


@router.get(
    "/",
    response_model=list[MedicationResponse],
)
def get_medications(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return medication_service.get_patient_medications(
        db,
        patient.id,
    )


@router.get(
    "/{medication_id}",
    response_model=MedicationResponse,
)
def get_medication(
    medication_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    medication = medication_service.get_patient_medication(
        db,
        patient.id,
        medication_id,
    )

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found.",
        )

    return medication


@router.put(
    "/{medication_id}",
    response_model=MedicationResponse,
)
def update_medication(
    medication_id: UUID,
    medication_data: MedicationUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    medication = medication_service.get_patient_medication(
        db,
        patient.id,
        medication_id,
    )

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found.",
        )

    return medication_service.update_medication(
        db,
        medication,
        medication_data,
    )


@router.delete(
    "/{medication_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_medication(
    medication_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    medication = medication_service.get_patient_medication(
        db,
        patient.id,
        medication_id,
    )

    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Medication not found.",
        )

    medication_service.delete(
        db,
        medication,
    )