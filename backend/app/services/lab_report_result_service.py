from app.common.base_service import BaseService
from app.models.lab_report_result import LabReportResult


class LabReportResultService(BaseService[LabReportResult]):
    def __init__(self):
        super().__init__(LabReportResult)


lab_report_result_service = LabReportResultService()