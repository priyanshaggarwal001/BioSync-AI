from app.common.base_service import BaseService
from app.models.vaccination import Vaccination


class VaccinationService(BaseService[Vaccination]):
    def __init__(self):
        super().__init__(Vaccination)


vaccination_service = VaccinationService()