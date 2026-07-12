from app.common.base_service import BaseService
from app.models.prescription import Prescription


class PrescriptionService(BaseService[Prescription]):
    def __init__(self):
        super().__init__(Prescription)


prescription_service = PrescriptionService()