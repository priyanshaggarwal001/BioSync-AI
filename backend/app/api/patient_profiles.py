from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.patient_profile import (
    PatientProfileCreate,
    PatientProfileResponse,
    PatientProfileUpdate,
)
from app.services.patient_profile_service import patient_profile_service


router = APIRouter(
    prefix="/patient-profiles",
    tags=["Patient Profiles"],
)


@router.post(
    "/",
    response_model=PatientProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_patient_profile(
    profile_data: PatientProfileCreate,
    db: Session = Depends(get_db),
):
    existing = patient_profile_service.get_by_user_id(
        db,
        profile_data.user_id,
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient profile already exists for this user.",
        )

    return patient_profile_service.create_profile(
        db,
        profile_data,
    )


@router.get(
    "/",
    response_model=list[PatientProfileResponse],
)
def get_patient_profiles(
    db: Session = Depends(get_db),
):
    return patient_profile_service.get_all(db)


@router.get(
    "/{profile_id}",
    response_model=PatientProfileResponse,
)
def get_patient_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
):
    profile = patient_profile_service.get_by_id(
        db,
        profile_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found.",
        )

    return profile


@router.put(
    "/{profile_id}",
    response_model=PatientProfileResponse,
)
def update_patient_profile(
    profile_id: UUID,
    profile_data: PatientProfileUpdate,
    db: Session = Depends(get_db),
):
    profile = patient_profile_service.get_by_id(
        db,
        profile_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found.",
        )

    return patient_profile_service.update_profile(
        db,
        profile,
        profile_data,
    )


@router.delete(
    "/{profile_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_patient_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
):
    profile = patient_profile_service.get_by_id(
        db,
        profile_id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found.",
        )

    patient_profile_service.delete(
        db,
        profile,
    )