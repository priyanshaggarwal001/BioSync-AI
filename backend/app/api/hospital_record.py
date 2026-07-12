from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.hospital_record import HospitalRecord
from app.schemas.hospital_record import (
    HospitalRecordCreate,
    HospitalRecordResponse,
    HospitalRecordUpdate,
)
from app.services.hospital_record_service import (
    hospital_record_service,
)

router = APIRouter(
    prefix="/hospital-records",
    tags=["Hospital Records"],
)


@router.post("/", response_model=HospitalRecordResponse)
def create_hospital_record(
    hospital_record: HospitalRecordCreate,
    db: Session = Depends(get_db),
):
    record = HospitalRecord(**hospital_record.model_dump())
    return hospital_record_service.create(db, record)


@router.get("/", response_model=list[HospitalRecordResponse])
def get_hospital_records(
    db: Session = Depends(get_db),
):
    return hospital_record_service.get_all(db)


@router.get("/{record_id}", response_model=HospitalRecordResponse)
def get_hospital_record(
    record_id: UUID,
    db: Session = Depends(get_db),
):
    return hospital_record_service.get_by_id(
        db,
        record_id,
    )


@router.put("/{record_id}", response_model=HospitalRecordResponse)
def update_hospital_record(
    record_id: UUID,
    hospital_record: HospitalRecordUpdate,
    db: Session = Depends(get_db),
):
    return hospital_record_service.update(
        db,
        record_id,
        hospital_record.model_dump(exclude_unset=True),
    )


@router.delete("/{record_id}")
def delete_hospital_record(
    record_id: UUID,
    db: Session = Depends(get_db),
):
    hospital_record_service.delete(db, record_id)
    return {
        "message": "Hospital record deleted successfully"
    }