from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.wearable_data import (
    WearableDataCreate,
    WearableDataResponse,
    WearableDataUpdate,
)
from app.services.wearable_data_service import wearable_data_service

router = APIRouter(
    prefix="/wearable-data",
    tags=["Wearable Data"],
)


@router.post(
    "/",
    response_model=WearableDataResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_wearable_data(
    wearable_data: WearableDataCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return wearable_data_service.create_wearable_data(
        db,
        patient,
        wearable_data,
        
        
    )


@router.get(
    "/",
    response_model=list[WearableDataResponse],
)
def get_wearable_data(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return wearable_data_service.get_patient_wearable_data_list(
        db,
        patient.id,
    )


@router.get(
    "/{wearable_data_id}",
    response_model=WearableDataResponse,
)
def get_wearable_data_by_id(
    wearable_data_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    wearable = wearable_data_service.get_patient_wearable_data(
        db,
        patient.id,
        wearable_data_id,
    )

    if not wearable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wearable data not found.",
        )

    return wearable


@router.put(
    "/{wearable_data_id}",
    response_model=WearableDataResponse,
)
def update_wearable_data(
    wearable_data_id: UUID,
    wearable_data: WearableDataUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    wearable = wearable_data_service.get_patient_wearable_data(
        db,
        patient.id,
        wearable_data_id,
    )

    if not wearable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wearable data not found.",
        )

    return wearable_data_service.update_wearable_data(
        db,
        wearable,
        wearable_data,
    )


@router.delete(
    "/{wearable_data_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_wearable_data(
    wearable_data_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    wearable = wearable_data_service.get_patient_wearable_data(
        db,
        patient.id,
        wearable_data_id,
    )

    if not wearable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wearable data not found.",
        )

    wearable_data_service.delete(
        db,
        wearable,
    )