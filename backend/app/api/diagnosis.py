from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.patient_profiles import PatientProfile
from app.api.dependencies import get_db
from app.schemas.diagnosis import (
    DiagnosisCreate,
    DiagnosisResponse,
    DiagnosisUpdate,
)
from app.services.diagnosis_service import diagnosis_service
from app.auth.dependencies import get_current_patient

router = APIRouter(
    prefix="/diagnoses",
    tags=["Diagnoses"],
)


@router.post(
    "/",
    response_model=DiagnosisResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_diagnosis(
    diagnosis_data: DiagnosisCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return diagnosis_service.create_diagnosis(
        db,
        diagnosis_data,
        patient
        
    )


@router.get(
    "/",
    response_model=list[DiagnosisResponse],
)
def get_diagnoses(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return diagnosis_service.get_patient_diagnoses(db, patient.id)


@router.get(
    "/{diagnosis_id}",
    response_model=DiagnosisResponse,
)
def get_diagnosis(
    diagnosis_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    diagnosis = diagnosis_service.get_patient_diagnosis(
        db,
        patient.id,
        diagnosis_id,
    )

    if not diagnosis:
        raise HTTPException(
            status_code=404,
            detail="Diagnosis not found.",
        )

    return diagnosis


@router.put(
    "/{diagnosis_id}",
    response_model=DiagnosisResponse,
)
def update_diagnosis(
    diagnosis_id: UUID,
    diagnosis_data: DiagnosisUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    diagnosis = diagnosis_service.get_patient_diagnosis(
        db,
        patient.id,
        diagnosis_id,
    )

    if not diagnosis:
        raise HTTPException(
            status_code=404,
            detail="Diagnosis not found.",
        )

    return diagnosis_service.update_diagnosis(
        db,
        diagnosis,
        diagnosis_data,
    )


@router.delete(
    "/{diagnosis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_diagnosis(
    diagnosis_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    diagnosis = diagnosis_service.get_patient_diagnosis(
        db,
        patient.id,
        diagnosis_id,
    )

    if not diagnosis:
        raise HTTPException(
            status_code=404,
            detail="Diagnosis not found.",
        )

    diagnosis_service.delete(
        db,
        diagnosis,
    )