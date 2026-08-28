from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.models.wearable_data import WearableData
from app.services.baseline_service import baseline_service


class HealthIntelligenceService:

    def calculate_wellness_score(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> int:

        wearable = (
            db.query(WearableData)
            .filter(
                WearableData.patient_id == patient.id,
            )
            .order_by(WearableData.recorded_at.desc())
            .first()
        )

        if not wearable:
            return 0

        baseline_data = baseline_service.get_wearable_baseline(
            db,
            patient,
        )

        baseline = baseline_data["baseline"]

        score = 0
        total_weight = 0

        # --------------------------------
        # Sleep
        # --------------------------------

        if (
            wearable.sleep_hours is not None
            and baseline.get("sleep_hours") is not None
        ):
            total_weight += 25

            current = wearable.sleep_hours
            base = baseline["sleep_hours"]

            if current >= base:
                score += 25
            elif current >= base * 0.90:
                score += 20
            elif current >= base * 0.80:
                score += 12
            else:
                score += 5

        # --------------------------------
        # Steps
        # --------------------------------

        if (
            wearable.steps is not None
            and baseline.get("steps") is not None
        ):
            total_weight += 20

            current = wearable.steps
            base = baseline["steps"]

            if current >= base:
                score += 20
            elif current >= base * 0.90:
                score += 16
            elif current >= base * 0.75:
                score += 10
            else:
                score += 5

        # --------------------------------
        # HRV
        # --------------------------------

        if (
            wearable.heart_rate_variability is not None
            and baseline.get("heart_rate_variability") is not None
        ):
            total_weight += 20

            current = wearable.heart_rate_variability
            base = baseline["heart_rate_variability"]

            if current >= base:
                score += 20
            elif current >= base * 0.90:
                score += 16
            elif current >= base * 0.75:
                score += 10
            else:
                score += 5

        # --------------------------------
        # Stress
        # Lower stress is better
        # --------------------------------

        if (
            wearable.stress_level is not None
            and baseline.get("stress_level") is not None
        ):
            total_weight += 20

            current = wearable.stress_level
            base = baseline["stress_level"]

            if current <= base:
                score += 20
            elif current <= base * 1.10:
                score += 16
            elif current <= base * 1.25:
                score += 10
            else:
                score += 5

        # --------------------------------
        # Resting Heart Rate
        # Closer to baseline is better
        # --------------------------------

        if (
            wearable.resting_heart_rate is not None
            and baseline.get("resting_heart_rate") is not None
        ):
            total_weight += 15

            current = wearable.resting_heart_rate
            base = baseline["resting_heart_rate"]

            difference = abs(current - base)

            if difference <= 3:
                score += 15
            elif difference <= 7:
                score += 12
            elif difference <= 12:
                score += 8
            else:
                score += 4

        if total_weight == 0:
            return 0

        return round(
            (score / total_weight) * 100
        )


health_intelligence_service = HealthIntelligenceService()