from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.lab_report import LabReport
from app.schemas.lab_report import (
    LabReportCreate,
    LabReportResponse,
    LabReportUpdate,
)
from app.services.lab_report_service import lab_report_service

router = APIRouter(
    prefix="/lab-reports",
    tags=["Lab Reports"],
)


@router.post("/", response_model=LabReportResponse)
def create_lab_report(
    lab_report: LabReportCreate,
    db: Session = Depends(get_db),
):
    report = LabReport(**lab_report.model_dump())
    return lab_report_service.create(db, report)


@router.get("/", response_model=list[LabReportResponse])
def get_lab_reports(
    db: Session = Depends(get_db),
):
    return lab_report_service.get_all(db)


@router.get("/{report_id}", response_model=LabReportResponse)
def get_lab_report(
    report_id: UUID,
    db: Session = Depends(get_db),
):
    return lab_report_service.get_by_id(
        db,
        report_id,
    )


@router.put("/{report_id}", response_model=LabReportResponse)
def update_lab_report(
    report_id: UUID,
    lab_report: LabReportUpdate,
    db: Session = Depends(get_db),
):
    return lab_report_service.update(
        db,
        report_id,
        lab_report.model_dump(exclude_unset=True),
    )


@router.delete("/{report_id}")
def delete_lab_report(
    report_id: UUID,
    db: Session = Depends(get_db),
):
    lab_report_service.delete(
        db,
        report_id,
    )
    return {
        "message": "Lab report deleted successfully"
    }