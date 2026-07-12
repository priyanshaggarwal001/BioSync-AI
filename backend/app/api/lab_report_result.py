from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.lab_report_result import LabReportResult
from app.schemas.lab_report_result import (
    LabReportResultCreate,
    LabReportResultResponse,
    LabReportResultUpdate,
)
from app.services.lab_report_result_service import (
    lab_report_result_service,
)

router = APIRouter(
    prefix="/lab-report-results",
    tags=["Lab Report Results"],
)


@router.post("/", response_model=LabReportResultResponse)
def create_lab_report_result(
    lab_report_result: LabReportResultCreate,
    db: Session = Depends(get_db),
):
    result = LabReportResult(**lab_report_result.model_dump())
    return lab_report_result_service.create(db, result)


@router.get("/", response_model=list[LabReportResultResponse])
def get_lab_report_results(
    db: Session = Depends(get_db),
):
    return lab_report_result_service.get_all(db)


@router.get("/{result_id}", response_model=LabReportResultResponse)
def get_lab_report_result(
    result_id: UUID,
    db: Session = Depends(get_db),
):
    return lab_report_result_service.get_by_id(
        db,
        result_id,
    )


@router.put("/{result_id}", response_model=LabReportResultResponse)
def update_lab_report_result(
    result_id: UUID,
    lab_report_result: LabReportResultUpdate,
    db: Session = Depends(get_db),
):
    return lab_report_result_service.update(
        db,
        result_id,
        lab_report_result.model_dump(exclude_unset=True),
    )


@router.delete("/{result_id}")
def delete_lab_report_result(
    result_id: UUID,
    db: Session = Depends(get_db),
):
    lab_report_result_service.delete(
        db,
        result_id,
    )
    return {
        "message": "Lab report result deleted successfully"
    }