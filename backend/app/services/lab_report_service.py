from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.common.base_service import BaseService
from app.models.lab_report import LabReport
from app.models.patient_profiles import PatientProfile
from app.schemas.lab_report import (
    LabReportCreate,
    LabReportUpdate,
)


class LabReportService(BaseService[LabReport]):
    def __init__(self):
        super().__init__(LabReport)

    def create_lab_report(
        self,
        db: Session,
        patient: PatientProfile,
        lab_report_data: LabReportCreate,
    ) -> LabReport:

        lab_report = LabReport(
            patient_id=patient.id,
            **lab_report_data.model_dump(),
        )

        return self.create(
            db,
            lab_report,
        )

    def get_patient_lab_report(
        self,
        db: Session,
        patient_id: UUID,
        report_id: UUID,
    ) -> LabReport | None:

        statement = (
            select(LabReport)
            .where(
                LabReport.id == report_id,
                LabReport.patient_id == patient_id,
            )
        )

        return db.scalar(statement)

    def get_patient_lab_reports(
        self,
        db: Session,
        patient_id: UUID,
    ) -> list[LabReport]:

        statement = (
            select(LabReport)
            .where(LabReport.patient_id == patient_id)
        )

        return list(db.scalars(statement).all())

    def update_lab_report(
        self,
        db: Session,
        lab_report: LabReport,
        lab_report_data: LabReportUpdate,
    ) -> LabReport:

        updates = lab_report_data.model_dump(
            exclude_unset=True
        )

        return self.update(
            db,
            lab_report,
            updates,
        )


lab_report_service = LabReportService()