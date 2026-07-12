from app.common.base_service import BaseService
from app.models.vital_sign import VitalSign

class VitalSignService(BaseService[VitalSign]):
    def __init__(self):
        super().__init__(VitalSign) 

vital_sign_service = VitalSignService()