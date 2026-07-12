from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.schemas.allergy import (
    AllergyCreate,
    AllergyResponse,
    AllergyUpdate,
)
from app.services.allergy_service import allergy_service

router = APIRouter(
    prefix="/allergies",
    tags=["Allergies"],
)


@router.post(
    "/",
    response_model=AllergyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_allergy(
    allergy_data: AllergyCreate,
    db: Session = Depends(get_db),
):
    return allergy_service.create_allergy(
        db,
        allergy_data,
    )


@router.get(
    "/",
    response_model=list[AllergyResponse],
)
def get_allergies(
    db: Session = Depends(get_db),
):
    return allergy_service.get_all(db)


@router.get(
    "/{allergy_id}",
    response_model=AllergyResponse,
)
def get_allergy(
    allergy_id: UUID,
    db: Session = Depends(get_db),
):
    allergy = allergy_service.get_by_id(
        db,
        allergy_id,
    )

    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found.",
        )

    return allergy


@router.put(
    "/{allergy_id}",
    response_model=AllergyResponse,
)
def update_allergy(
    allergy_id: UUID,
    allergy_data: AllergyUpdate,
    db: Session = Depends(get_db),
):
    allergy = allergy_service.get_by_id(
        db,
        allergy_id,
    )

    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found.",
        )

    return allergy_service.update_allergy(
        db,
        allergy,
        allergy_data,
    )


@router.delete(
    "/{allergy_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_allergy(
    allergy_id: UUID,
    db: Session = Depends(get_db),
):
    allergy = allergy_service.get_by_id(
        db,
        allergy_id,
    )

    if not allergy:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Allergy not found.",
        )

    allergy_service.delete(
        db,
        allergy,
    )
    