from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db
from app.auth.dependencies import get_current_patient
from app.models.patient_profiles import PatientProfile
from app.schemas.dashboard import DashboardResponse
from app.services.dashboard_service import dashboard_service
from app.services.trend_service import trend_service
from app.services.insight_service import insight_service
from app.services.baseline_service import baseline_service
from app.services.ai_service import ai_service
router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/",
    response_model=DashboardResponse,
)
def get_dashboard(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return dashboard_service.get_dashboard(
        db,
        patient,
    )


@router.get(
    "/trends",
)
def get_dashboard_trends(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return trend_service.get_wearable_trends(
        db,
        patient,
    )

@router.get(
    "/insights",
)
def get_dashboard_insights(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return insight_service.get_health_insights(
        db,
        patient,
    )
@router.get(
    "/baseline",
)
def get_dashboard_baseline(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return baseline_service.get_wearable_baseline(
        db,
        patient,
    )

@router.get(
    "/ai-summary",
)
async def get_dashboard_ai_summary(

    patient: PatientProfile = Depends(get_current_patient),

    db: Session = Depends(get_db),

):

    return await ai_service.generate_health_summary(

        db,

        patient,

    )


@router.get(
    "/guidance",
)
async def get_dashboard_guidance(
    patient: PatientProfile = Depends(get_current_patient),
    db: Session = Depends(get_db),
):
    return await ai_service.generate_actionable_guidance(
        db,
        patient,
    )
