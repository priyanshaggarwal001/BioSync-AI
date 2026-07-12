from app.common.base_service import BaseService
from app.models.lab_report import LabReport


class LabReportService(BaseService[LabReport]):
    def __init__(self):
        super().__init__(LabReport)


lab_report_service = LabReportService()