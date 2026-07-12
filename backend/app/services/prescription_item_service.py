from app.common.base_service import BaseService
from app.models.prescription_item import PrescriptionItem


class PrescriptionItemService(BaseService[PrescriptionItem]):
    def __init__(self):
        super().__init__(PrescriptionItem)


prescription_item_service = PrescriptionItemService()