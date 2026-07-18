from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.hospital_record import (
    HospitalRecordCreate,
    HospitalRecordResponse,
    HospitalRecordUpdate,
)
from app.services.hospital_record_service import (
    hospital_record_service,
)

router = APIRouter(
    prefix="/hospital-records",
    tags=["Hospital Records"],
)


@router.post(
    "/",
    response_model=HospitalRecordResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_hospital_record(
    hospital_record_data: HospitalRecordCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return hospital_record_service.create_hospital_record(
        db,
        patient,
        hospital_record_data,
        
       
    )


@router.get(
    "/",
    response_model=list[HospitalRecordResponse],
)
def get_hospital_records(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return hospital_record_service.get_patient_hospital_records(
        db,
        patient.id,
    )


@router.get(
    "/{record_id}",
    response_model=HospitalRecordResponse,
)
def get_hospital_record(
    record_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    hospital_record = hospital_record_service.get_patient_hospital_record(
        db,
        patient.id,
        record_id,
    )

    if not hospital_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital record not found.",
        )

    return hospital_record


@router.put(
    "/{record_id}",
    response_model=HospitalRecordResponse,
)
def update_hospital_record(
    record_id: UUID,
    hospital_record_data: HospitalRecordUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    hospital_record = hospital_record_service.get_patient_hospital_record(
        db,
        patient.id,
        record_id,
    )

    if not hospital_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital record not found.",
        )

    return hospital_record_service.update_hospital_record(
        db,
        hospital_record,
        hospital_record_data,
    )


@router.delete(
    "/{record_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_hospital_record(
    record_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    hospital_record = hospital_record_service.get_patient_hospital_record(
        db,
        patient.id,
        record_id,
    )

    if not hospital_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Hospital record not found.",
        )

    hospital_record_service.delete(
        db,
        hospital_record,
    )