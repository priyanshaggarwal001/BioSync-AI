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
from app.auth.dependencies import get_current_user
from app.models.user import User

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
    current_user: User = Depends(get_current_user),
):
    existing = patient_profile_service.get_by_user_id(
    db,
    current_user.id,
)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Patient profile already exists for this user.",
        )

    return patient_profile_service.create_profile(
    db,
    current_user,
    profile_data,
    
    
)


@router.get(
    "/me",
    response_model=PatientProfileResponse,
)
def get_my_patient_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    profile = patient_profile_service.get_by_user_id(
        db,
        current_user.id,
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Patient profile not found.",
        )

    return profile


@router.get(
    "/{profile_id}",
    response_model=PatientProfileResponse,
)
def get_patient_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
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

    if profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to access this profile.",
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
    current_user: User = Depends(get_current_user),
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

    if profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to update this profile.",
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
    current_user: User = Depends(get_current_user),
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