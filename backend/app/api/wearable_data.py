from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.wearable_data import WearableData
from app.schemas.wearable_data import (
    WearableDataCreate,
    WearableDataResponse,
    WearableDataUpdate,
)
from app.services.wearable_data_service import wearable_data_service

router = APIRouter(
    prefix="/wearable-data",
    tags=["Wearable Data"],
)


@router.post("/", response_model=WearableDataResponse)
def create_wearable_data(
    wearable_data: WearableDataCreate,
    db: Session = Depends(get_db),
):
    wearable = WearableData(**wearable_data.model_dump())
    return wearable_data_service.create(db, wearable)


@router.get("/", response_model=list[WearableDataResponse])
def get_wearable_data(
    db: Session = Depends(get_db),
):
    return wearable_data_service.get_all(db)


@router.get("/{wearable_data_id}", response_model=WearableDataResponse)
def get_wearable_data_by_id(
    wearable_data_id: UUID,
    db: Session = Depends(get_db),
):
    return wearable_data_service.get_by_id(
        db,
        wearable_data_id,
    )


@router.put("/{wearable_data_id}", response_model=WearableDataResponse)
def update_wearable_data(
    wearable_data_id: UUID,
    wearable_data: WearableDataUpdate,
    db: Session = Depends(get_db),
):
    return wearable_data_service.update(
        db,
        wearable_data_id,
        wearable_data.model_dump(exclude_unset=True),
    )


@router.delete("/{wearable_data_id}")
def delete_wearable_data(
    wearable_data_id: UUID,
    db: Session = Depends(get_db),
):
    wearable_data_service.delete(db, wearable_data_id)
    return {
        "message": "Wearable data deleted successfully"
    }