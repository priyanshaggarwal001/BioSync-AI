from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.models.vaccination import Vaccination
from app.schemas.vaccination import (
    VaccinationCreate,
    VaccinationResponse,
    VaccinationUpdate,
)
from app.services.vaccination_service import vaccination_service

router = APIRouter(
    prefix="/vaccinations",
    tags=["Vaccinations"],
)


@router.post("/", response_model=VaccinationResponse)
def create_vaccination(
    vaccination: VaccinationCreate,
    db: Session = Depends(get_db),
):
    vaccination_obj = Vaccination(**vaccination.model_dump())
    return vaccination_service.create(db, vaccination_obj)


@router.get("/", response_model=list[VaccinationResponse])
def get_vaccinations(
    db: Session = Depends(get_db),
):
    return vaccination_service.get_all(db)


@router.get("/{vaccination_id}", response_model=VaccinationResponse)
def get_vaccination(
    vaccination_id: UUID,
    db: Session = Depends(get_db),
):
    return vaccination_service.get_by_id(
        db,
        vaccination_id,
    )


@router.put("/{vaccination_id}", response_model=VaccinationResponse)
def update_vaccination(
    vaccination_id: UUID,
    vaccination: VaccinationUpdate,
    db: Session = Depends(get_db),
):
    return vaccination_service.update(
        db,
        vaccination_id,
        vaccination.model_dump(exclude_unset=True),
    )


@router.delete("/{vaccination_id}")
def delete_vaccination(
    vaccination_id: UUID,
    db: Session = Depends(get_db),
):
    vaccination_service.delete(db, vaccination_id)
    return {
        "message": "Vaccination deleted successfully"
    }