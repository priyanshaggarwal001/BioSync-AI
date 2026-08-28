from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.models.vital_sign import VitalSign
from app.models.wearable_data import WearableData
from app.models.medication import Medication
from app.models.diagnosis import Diagnosis
from app.services.insight_service import insight_service
from app.services.timeline_service import timeline_service
from app.schemas.dashboard import DashboardResponse
from app.services.health_intelligence_service import (
    health_intelligence_service,
)


class DashboardService:

    def get_dashboard(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> DashboardResponse:

        latest_vital = (
            db.query(VitalSign)
            .filter(VitalSign.patient_id == patient.id)
            .order_by(VitalSign.recorded_at.desc())
            .first()
        )

        latest_wearable = (
            db.query(WearableData)
            .filter(WearableData.patient_id == patient.id)
            .order_by(WearableData.recorded_at.desc())
            .first()
        )

        active_medications = (
            db.query(Medication)
            .filter(
                Medication.patient_id == patient.id,
                Medication.is_active == True,
            )
            .count()
        )

        recent_diagnoses = (
            db.query(Diagnosis)
            .filter(Diagnosis.patient_id == patient.id)
            .count()
        )

        timeline = timeline_service.get_timeline(
            db,
            patient.id,
        )

        recent_events = [
            event.model_dump()
            for event in timeline.events[:5]
        ]

        wellness_score = (
            health_intelligence_service.calculate_wellness_score(
                db,
                patient,
            )
        )

        if wellness_score >= 80:
            wellness_score_status = "Good"
        elif wellness_score >= 60:
            wellness_score_status = "Moderate"
        else:
            wellness_score_status = "Needs Attention"

        insights = insight_service.get_health_insights(
            db,
            patient,
        )
        return DashboardResponse(
            patient_id=patient.id,
            patient_name=f"{patient.first_name} {patient.last_name}",

            wellness_score=wellness_score,
            wellness_score_status=wellness_score_status,

            latest_vital=(
                {
                    "recorded_at": latest_vital.recorded_at,
                    "heart_rate": latest_vital.heart_rate,
                    "systolic_bp": latest_vital.systolic_bp,
                    "diastolic_bp": latest_vital.diastolic_bp,
                    "body_temperature": latest_vital.body_temperature,
                    "oxygen_saturation": latest_vital.oxygen_saturation,
                    "bmi": latest_vital.bmi,
                }
                if latest_vital
                else None
            ),

            latest_wearable=(
                {
                    "recorded_at": latest_wearable.recorded_at,
                    "steps": latest_wearable.steps,
                    "sleep_hours": latest_wearable.sleep_hours,
                    "active_minutes": latest_wearable.active_minutes,
                    "resting_heart_rate": latest_wearable.resting_heart_rate,
                    "heart_rate_variability": latest_wearable.heart_rate_variability,
                    "stress_level": latest_wearable.stress_level,
                }
                if latest_wearable
                else None
            ),

            active_medications=active_medications,
            recent_diagnoses=recent_diagnoses,
            recent_events=recent_events,

            insights=insights
        )


dashboard_service = DashboardService()