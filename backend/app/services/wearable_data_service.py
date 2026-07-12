from app.common.base_service import BaseService
from app.models.wearable_data import WearableData


class WearableDataService(BaseService[WearableData]):
    def __init__(self):
        super().__init__(WearableData)


wearable_data_service = WearableDataService()