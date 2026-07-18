from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter(
    prefix="/health",
    tags=["Health Check"],
)


@router.get("/")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected",
            "service": "BioSync AI Backend",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed.",
        )