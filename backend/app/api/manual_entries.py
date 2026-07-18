from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.manual_entry import (
    ManualEntryCreate,
    ManualEntryResponse,
    ManualEntryUpdate,
)
from app.services.manual_entry_service import manual_entry_service

router = APIRouter(
    prefix="/manual-entries",
    tags=["Manual Entries"],
)


@router.post(
    "/",
    response_model=ManualEntryResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_manual_entry(
    entry_data: ManualEntryCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return manual_entry_service.create_entry(
        db,
        patient,
        entry_data,
        
        
    )


@router.get(
    "/",
    response_model=list[ManualEntryResponse],
)
def get_manual_entries(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return manual_entry_service.get_user_entries(
        db,
        patient.id,
    )


@router.get(
    "/{entry_id}",
    response_model=ManualEntryResponse,
)
def get_manual_entry(
    entry_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    entry = manual_entry_service.get_user_entry(
        db,
        patient.id,
        entry_id,
    )

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manual entry not found.",
        )

    return entry


@router.put(
    "/{entry_id}",
    response_model=ManualEntryResponse,
)
def update_manual_entry(
    entry_id: UUID,
    entry_data: ManualEntryUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    entry = manual_entry_service.get_user_entry(
        db,
        patient.id,
        entry_id,
    )

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manual entry not found.",
        )

    return manual_entry_service.update_entry(
        db,
        entry,
        entry_data,
    )


@router.delete(
    "/{entry_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_manual_entry(
    entry_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    entry = manual_entry_service.get_user_entry(
        db,
        patient.id,
        entry_id,
    )

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Manual entry not found.",
        )

    manual_entry_service.delete(
        db,
        entry,
    )