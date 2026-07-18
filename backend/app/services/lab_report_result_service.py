from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.lab_report import LabReport
from app.models.lab_report_result import LabReportResult
from app.models.patient_profiles import PatientProfile
from app.schemas.lab_report_result import (
    LabReportResultCreate,
    LabReportResultUpdate,
)


class LabReportResultService(BaseService[LabReportResult]):
    def __init__(self):
        super().__init__(LabReportResult)

    def create_lab_report_result(
        self,
        db: Session,
        patient: PatientProfile,
        result_data: LabReportResultCreate,
    ) -> LabReportResult:

        lab_report = db.scalar(
            select(LabReport).where(
                LabReport.id == result_data.lab_report_id,
                LabReport.patient_id == patient.id,
            )
        )

        if not lab_report:
            raise ValueError("Lab report not found.")

        result = LabReportResult(
            **result_data.model_dump(),
        )

        return self.create(
            db,
            result,
        )

    def get_lab_report_result(
        self,
        db: Session,
        patient_id: UUID,
        result_id: UUID,
    ) -> LabReportResult | None:

        statement = (
            select(LabReportResult)
            .join(LabReport)
            .where(
                LabReportResult.id == result_id,
                LabReport.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_lab_report_results(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[LabReportResult]:

        statement = (
            select(LabReportResult)
            .join(LabReport)
            .where(
                LabReport.patient_id == patient_id,
            )
        )

        return list(db.scalars(statement).all())

    def update_lab_report_result(
        self,
        db: Session,
        result: LabReportResult,
        result_data: LabReportResultUpdate,
    ) -> LabReportResult:

        updates = result_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            result,
            updates,
        )


lab_report_result_service = LabReportResultService()