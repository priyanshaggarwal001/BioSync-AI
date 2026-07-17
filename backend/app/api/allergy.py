from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.allergy import (
    AllergyCreate,
    AllergyResponse,
    AllergyUpdate,
)
from app.services.allergy_service import allergy_service

router = APIRouter(
    prefix="/allergies",
    tags=["Allergies"],
)


@router.post(
    "/",
    response_model=AllergyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_allergy(
    allergy_data: AllergyCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return allergy_service.create_allergy(
        db,
        patient,
        allergy_data,
    )


@router.get(
    "/",
    response_model=list[AllergyResponse],
)
def get_allergies(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return allergy_service.get_patient_allergies(
        db,
        patient.id,
    )


@router.get(
    "/{allergy_id}",
    response_model=AllergyResponse,
)
def get_allergy(
    allergy_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    allergy = allergy_service.get_patient_allergy(
        db,
        patient.id,
        allergy_id,
    )

    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found.",
        )

    return allergy


@router.put(
    "/{allergy_id}",
    response_model=AllergyResponse,
)
def update_allergy(
    allergy_id: UUID,
    allergy_data: AllergyUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    allergy = allergy_service.get_patient_allergy(
        db,
        patient.id,
        allergy_id,
)

    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found.",
        )

    return allergy_service.update_allergy(
        db,
        allergy,
        allergy_data,
    )


@router.delete(
    "/{allergy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_allergy(
    allergy_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    allergy = allergy_service.get_patient_allergy(
        db,
        patient.id,
        allergy_id,
    )

    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found.",
        )

    allergy_service.delete(
        db,
        allergy,
    )