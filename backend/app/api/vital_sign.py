from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.vital_sign import VitalSign
from app.schemas.vital_sign import (
    VitalSignCreate,
    VitalSignResponse,
    VitalSignUpdate,
)
from app.services.vital_sign_service import vital_sign_service

router = APIRouter(
    prefix="/vital-signs",
    tags=["Vital Signs"],
)


@router.post("/", response_model=VitalSignResponse)
def create_vital_sign(
    vital_sign: VitalSignCreate,
    db: Session = Depends(get_db),
):
    vital = VitalSign(**vital_sign.model_dump())
    return vital_sign_service.create(db, vital)


@router.get("/", response_model=list[VitalSignResponse])
def get_vital_signs(
    db: Session = Depends(get_db),
):
    return vital_sign_service.get_all(db)


@router.get("/{vital_sign_id}", response_model=VitalSignResponse)
def get_vital_sign(
    vital_sign_id: UUID,
    db: Session = Depends(get_db),
):
    return vital_sign_service.get_by_id(db, vital_sign_id)


@router.put("/{vital_sign_id}", response_model=VitalSignResponse)
def update_vital_sign(
    vital_sign_id: UUID,
    vital_sign: VitalSignUpdate,
    db: Session = Depends(get_db),
):
    return vital_sign_service.update(
        db,
        vital_sign_id,
        vital_sign.model_dump(exclude_unset=True),
    )


@router.delete("/{vital_sign_id}")
def delete_vital_sign(
    vital_sign_id: UUID,
    db: Session = Depends(get_db),
):
    vital_sign_service.delete(db, vital_sign_id)
    return {"message": "Vital sign deleted successfully"}