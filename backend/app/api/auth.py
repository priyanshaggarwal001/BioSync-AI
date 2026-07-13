from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.jwt import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth import TokenResponse
from app.services.user_service import user_service

from app.auth.dependencies import get_current_user
from app.models.user import User



router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)
@router.post(
    "/login",
    response_model=TokenResponse,
)
@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = user_service.authenticate_user(
        db,
        form_data.username,
        form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
    {
        "sub": user.email,
        "user_id": str(user.id),
    }
)

    return TokenResponse(
        access_token=access_token,
    )

@router.get("/me")
def me(
    current_user: User = Depends(get_current_user),
):
    return {
        "id": str(current_user.id),
        "email": current_user.email,
    }