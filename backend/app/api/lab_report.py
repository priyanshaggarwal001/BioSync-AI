from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.lab_report import (
    LabReportCreate,
    LabReportResponse,
    LabReportUpdate,
)
from app.services.lab_report_service import (
    lab_report_service,
)

router = APIRouter(
    prefix="/lab-reports",
    tags=["Lab Reports"],
)


@router.post(
    "/",
    response_model=LabReportResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lab_report(
    lab_report_data: LabReportCreate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return lab_report_service.create_lab_report(
        db,
        patient,
        lab_report_data,
        
       
    )


@router.get(
    "/",
    response_model=list[LabReportResponse],
)
def get_lab_reports(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return lab_report_service.get_patient_lab_reports(
        db,
        patient.id,
    )


@router.get(
    "/{report_id}",
    response_model=LabReportResponse,
)
def get_lab_report(
    report_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    lab_report = lab_report_service.get_patient_lab_report(
        db,
        patient.id,
        report_id,
    )

    if not lab_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab report not found.",
        )

    return lab_report


@router.put(
    "/{report_id}",
    response_model=LabReportResponse,
)
def update_lab_report(
    report_id: UUID,
    lab_report_data: LabReportUpdate,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    lab_report = lab_report_service.get_patient_lab_report(
        db,
        patient.id,
        report_id,
    )

    if not lab_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab report not found.",
        )

    return lab_report_service.update_lab_report(
        db,
        lab_report,
        lab_report_data,
    )


@router.delete(
    "/{report_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_lab_report(
    report_id: UUID,
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    lab_report = lab_report_service.get_patient_lab_report(
        db,
        patient.id,
        report_id,
    )

    if not lab_report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lab report not found.",
        )

    lab_report_service.delete(
        db,
        lab_report,
    )