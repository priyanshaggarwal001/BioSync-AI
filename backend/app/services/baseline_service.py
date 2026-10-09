from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.models.wearable_data import WearableData


class BaselineService:

    def get_wearable_baseline(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> dict:

        # --------------------------------
        # Get latest 15 records
        #
        # Latest record = current measurement
        # Remaining 14 records = baseline
        # --------------------------------

        records = (
            db.query(WearableData)
            .filter(
                WearableData.patient_id == patient.id,
            )
            .order_by(WearableData.recorded_at.desc())
            .limit(15)
            .all()
        )

        if len(records) <= 1:
            return {
                "records_analyzed": 0,
                "baseline": {},
            }

        # --------------------------------
        # Exclude the latest/current record
        # --------------------------------

        baseline_records = records[1:]

        # --------------------------------
        # Average helper
        # --------------------------------

        def average(values):

            if not values:
                return None

            return round(
                sum(values) / len(values),
                2,
            )

        # --------------------------------
        # Sleep
        # --------------------------------

        sleep_values = [
            record.sleep_hours
            for record in baseline_records
            if record.sleep_hours is not None
        ]

        # --------------------------------
        # Steps
        # --------------------------------

        step_values = [
            record.steps
            for record in baseline_records
            if record.steps is not None
        ]

        # --------------------------------
        # Stress
        # --------------------------------

        stress_values = [
            record.stress_level
            for record in baseline_records
            if record.stress_level is not None
        ]

        # --------------------------------
        # Resting Heart Rate
        # --------------------------------

        resting_hr_values = [
            record.resting_heart_rate
            for record in baseline_records
            if record.resting_heart_rate is not None
        ]

        # --------------------------------
        # HRV
        # --------------------------------

        hrv_values = [
            record.heart_rate_variability
            for record in baseline_records
            if record.heart_rate_variability is not None
        ]

        # --------------------------------
        # Active Minutes
        # --------------------------------

        active_minutes_values = [
            record.active_minutes
            for record in baseline_records
            if record.active_minutes is not None
        ]

        # --------------------------------
        # VO2 Max
        # --------------------------------

        vo2_values = [
            record.vo2_max
            for record in baseline_records
            if record.vo2_max is not None
        ]

        # --------------------------------
        # Return baseline
        # --------------------------------

        return {
            "records_analyzed": len(baseline_records),

            "baseline": {
                "sleep_hours": average(
                    sleep_values
                ),

                "steps": average(
                    step_values
                ),

                "stress_level": average(
                    stress_values
                ),

                "resting_heart_rate": average(
                    resting_hr_values
                ),

                "heart_rate_variability": average(
                    hrv_values
                ),

                "active_minutes": average(
                    active_minutes_values
                ),

                "vo2_max": average(
                    vo2_values
                ),
            },
        }


baseline_service = BaselineService()