from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.vital_sign import VitalSign
from app.schemas.vital_sign import (
    VitalSignCreate,
    VitalSignResponse,
    VitalSignUpdate,
)
from app.services.vital_sign_service import vital_sign_service
from app.models.patient_profiles import PatientProfile
from app.auth.dependencies import get_current_patient
router = APIRouter(
    prefix="/vital-signs",
    tags=["Vital Signs"],
)


@router.post(
        "/", 
        response_model=VitalSignResponse,
        status_code=status.HTTP_201_CREATED,
)
def create_vital_sign(
    vital_sign: VitalSignCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
   return vital_sign_service.create_vital_sign(
        db,
        patient,
        vital_sign,
        
        
    )


@router.get(
        "/", 
        response_model=list[VitalSignResponse],
        )
def get_vital_signs(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return vital_sign_service.get_patient_vital_signs(
        db,
        patient.id,
    )


@router.get(
        "/{vital_sign_id}", 
        response_model=VitalSignResponse,
        )
def get_vital_sign(
    
    vital_sign_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return vital_sign_service.get_patient_vital_sign(
        db,
        patient.id,
        vital_sign_id
    )
    if not vital_sign:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vital sign not found",
        )
    return vital_sign


@router.put(
        "/{vital_sign_id}", 
        response_model=VitalSignResponse,
        )
def update_vital_sign(
    vital_sign_id: UUID,
    vital_sign: VitalSignUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    vital=vital_sign_service.get_patient_vital_sign(
        db,
        patient.id,
        vital_sign_id
    )
    if not vital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vital sign not found",
        )
    return vital_sign_service.update_vital_sign(
        db,
        vital,
        vital_sign,
    )


@router.delete(
        "/{vital_sign_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        )
def delete_vital_sign(
    vital_sign_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    vital=vital_sign_service.get_patient_vital_sign(
        db,
        patient.id,
        vital_sign_id
    )
    if not vital:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vital sign not found",
        )
    vital_sign_service.delete_vital_sign(
        db,
        vital,
    )