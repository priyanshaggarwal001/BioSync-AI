from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_patient
from app.database.session import get_db
from app.models.patient_profiles import PatientProfile
from app.schemas.vaccination import (
    VaccinationCreate,
    VaccinationResponse,
    VaccinationUpdate,
)
from app.services.vaccination_service import vaccination_service

router = APIRouter(
    prefix="/vaccinations",
    tags=["Vaccinations"],
)


@router.post(
    "/",
    response_model=VaccinationResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_vaccination(
    vaccination: VaccinationCreate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(get_current_patient),
):
    return vaccination_service.create_vaccination(
        db,
        patient.
        vaccination,
        
        
    )


@router.get(
    "/",
    response_model=list[VaccinationResponse],
)
def get_vaccinations(
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(get_current_patient),
):
    return vaccination_service.get_patient_vaccinations(
        db,
        patient.id,
    )


@router.get(
    "/{vaccination_id}",
    response_model=VaccinationResponse,
)
def get_vaccination(
    vaccination_id: UUID,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(get_current_patient),
):
    vaccination = vaccination_service.get_patient_vaccination(
        db,
        patient.id,
        vaccination_id,
    )

    if vaccination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaccination not found",
        )

    return vaccination


@router.put(
    "/{vaccination_id}",
    response_model=VaccinationResponse,
)
def update_vaccination(
    vaccination_id: UUID,
    vaccination_data: VaccinationUpdate,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(get_current_patient),
):
    vaccination = vaccination_service.get_patient_vaccination(
        db,
        patient.id,
        vaccination_id,
    )

    if vaccination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaccination not found",
        )

    return vaccination_service.update_vaccination(
        db,
        vaccination,
        vaccination_data,
    )


@router.delete(
    "/{vaccination_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_vaccination(
    vaccination_id: UUID,
    db: Session = Depends(get_db),
    patient: PatientProfile = Depends(get_current_patient),
):
    vaccination = vaccination_service.get_patient_vaccination(
        db,
        patient.id,
        vaccination_id,
    )

    if vaccination is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vaccination not found",
        )

    vaccination_service.delete(
        db,
        vaccination,
    )