from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.models.wearable_data import WearableData


class BaselineService:

    def get_wearable_baseline(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> dict:

        records = (
            db.query(WearableData)
            .filter(
                WearableData.patient_id == patient.id,
            )
            .order_by(WearableData.recorded_at.desc())
            .limit(14)
            .all()
        )

        if not records:
            return {
                "records_analyzed": 0,
                "baseline": {},
            }

        def average(values):
            if not values:
                return None

            return round(
                sum(values) / len(values),
                2,
            )

        sleep_values = [
            record.sleep_hours
            for record in records
            if record.sleep_hours is not None
        ]

        step_values = [
            record.steps
            for record in records
            if record.steps is not None
        ]

        stress_values = [
            record.stress_level
            for record in records
            if record.stress_level is not None
        ]

        resting_hr_values = [
            record.resting_heart_rate
            for record in records
            if record.resting_heart_rate is not None
        ]

        hrv_values = [
            record.heart_rate_variability
            for record in records
            if record.heart_rate_variability is not None
        ]

        active_minutes_values = [
            record.active_minutes
            for record in records
            if record.active_minutes is not None
        ]

        vo2_values = [
            record.vo2_max
            for record in records
            if record.vo2_max is not None
        ]

        return {
            "records_analyzed": len(records),
            "baseline": {
                "sleep_hours": average(sleep_values),
                "steps": average(step_values),
                "stress_level": average(stress_values),
                "resting_heart_rate": average(resting_hr_values),
                "heart_rate_variability": average(hrv_values),
                "active_minutes": average(active_minutes_values),
                "vo2_max": average(vo2_values),
            },
        }


baseline_service = BaselineService()