from app.common.base_service import BaseService
from app.models.hospital_record import HospitalRecord


class HospitalRecordService(BaseService[HospitalRecord]):
    def __init__(self):
        super().__init__(HospitalRecord)


hospital_record_service = HospitalRecordService()