from app.common.base_service import BaseService
from app.models.medication import Medication


class MedicationService(BaseService[Medication]):
    def __init__(self):
        super().__init__(Medication)


medication_service = MedicationService()