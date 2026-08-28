from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.models.wearable_data import WearableData


class TrendService:

    def get_wearable_trends(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> dict:

        today = datetime.utcnow()

        current_start = today - timedelta(days=7)
        previous_start = today - timedelta(days=14)

        records = (
            db.query(WearableData)
            .filter(
                WearableData.patient_id == patient.id,
                WearableData.recorded_at >= previous_start,
                WearableData.recorded_at <= today,
            )
            .order_by(WearableData.recorded_at.asc())
            .all()
        )

        previous_records = [
            record
            for record in records
            if record.recorded_at < current_start
        ]

        current_records = [
            record
            for record in records
            if record.recorded_at >= current_start
        ]

        if not previous_records or not current_records:
            return {
                "period": "14 days",
                "previous_period": "Previous 7 days",
                "current_period": "Current 7 days",
                "records_analyzed": len(records),
                "trends": [],
            }

        trends = []

        # --------------------------------------------------
        # Helper function
        # --------------------------------------------------

        def calculate_trend(
            metric,
            previous_values,
            current_values,
            lower_is_better=False,
        ):

            if not previous_values or not current_values:
                return None

            previous_average = (
                sum(previous_values) / len(previous_values)
            )

            current_average = (
                sum(current_values) / len(current_values)
            )

            if previous_average == 0:
                return None

            percentage_change = (
                (current_average - previous_average)
                / previous_average
            ) * 100

            if lower_is_better:

                if percentage_change < -5:
                    direction = "Improving"
                elif percentage_change > 5:
                    direction = "Increasing"
                else:
                    direction = "Stable"

            else:

                if percentage_change > 5:
                    direction = "Improving"
                elif percentage_change < -5:
                    direction = "Declining"
                else:
                    direction = "Stable"

            return {
                "metric": metric,
                "previous_average": round(previous_average, 2),
                "current_average": round(current_average, 2),
                "percentage_change": round(percentage_change, 2),
                "direction": direction,
            }

        # --------------------------------------------------
        # Sleep
        # --------------------------------------------------

        previous_sleep = [
            r.sleep_hours
            for r in previous_records
            if r.sleep_hours is not None
        ]

        current_sleep = [
            r.sleep_hours
            for r in current_records
            if r.sleep_hours is not None
        ]

        trend = calculate_trend(
            "sleep",
            previous_sleep,
            current_sleep,
        )

        if trend:
            trends.append(trend)

        # --------------------------------------------------
        # Steps
        # --------------------------------------------------

        previous_steps = [
            r.steps
            for r in previous_records
            if r.steps is not None
        ]

        current_steps = [
            r.steps
            for r in current_records
            if r.steps is not None
        ]

        trend = calculate_trend(
            "steps",
            previous_steps,
            current_steps,
        )

        if trend:
            trends.append(trend)

        # --------------------------------------------------
        # Stress
        # Lower stress is better
        # --------------------------------------------------

        previous_stress = [
            r.stress_level
            for r in previous_records
            if r.stress_level is not None
        ]

        current_stress = [
            r.stress_level
            for r in current_records
            if r.stress_level is not None
        ]

        trend = calculate_trend(
            "stress",
            previous_stress,
            current_stress,
            lower_is_better=True,
        )

        if trend:
            trends.append(trend)

        # --------------------------------------------------
        # Resting Heart Rate
        # --------------------------------------------------

        previous_resting_hr = [
            r.resting_heart_rate
            for r in previous_records
            if r.resting_heart_rate is not None
        ]

        current_resting_hr = [
            r.resting_heart_rate
            for r in current_records
            if r.resting_heart_rate is not None
        ]

        trend = calculate_trend(
            "resting_heart_rate",
            previous_resting_hr,
            current_resting_hr,
        )

        if trend:
            trends.append(trend)

        # --------------------------------------------------
        # Heart Rate Variability
        # Higher HRV is generally treated as better
        # --------------------------------------------------

        previous_hrv = [
            r.heart_rate_variability
            for r in previous_records
            if r.heart_rate_variability is not None
        ]

        current_hrv = [
            r.heart_rate_variability
            for r in current_records
            if r.heart_rate_variability is not None
        ]

        trend = calculate_trend(
            "heart_rate_variability",
            previous_hrv,
            current_hrv,
        )

        if trend:
            trends.append(trend)

        # --------------------------------------------------
        # Active Minutes
        # --------------------------------------------------

        previous_active_minutes = [
            r.active_minutes
            for r in previous_records
            if r.active_minutes is not None
        ]

        current_active_minutes = [
            r.active_minutes
            for r in current_records
            if r.active_minutes is not None
        ]

        trend = calculate_trend(
            "active_minutes",
            previous_active_minutes,
            current_active_minutes,
        )

        if trend:
            trends.append(trend)

        # --------------------------------------------------
        # VO2 Max
        # --------------------------------------------------

        previous_vo2 = [
            r.vo2_max
            for r in previous_records
            if r.vo2_max is not None
        ]

        current_vo2 = [
            r.vo2_max
            for r in current_records
            if r.vo2_max is not None
        ]

        trend = calculate_trend(
            "vo2_max",
            previous_vo2,
            current_vo2,
        )

        if trend:
            trends.append(trend)

        return {
            "period": "14 days",
            "previous_period": "Previous 7 days",
            "current_period": "Current 7 days",
            "records_analyzed": len(records),
            "trends": trends,
        }


trend_service = TrendService()