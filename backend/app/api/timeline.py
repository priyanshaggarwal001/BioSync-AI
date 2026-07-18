from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_patient
from app.database.session import get_db
from app.models.patient_profiles import PatientProfile
from app.schemas.timeline import TimelineResponse
from app.services.timeline_service import timeline_service


router = APIRouter(
    prefix="/timeline",
    tags=["Timeline"],
)


@router.get("/", response_model=TimelineResponse)
def get_timeline(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return timeline_service.get_timeline(db, patient.id)