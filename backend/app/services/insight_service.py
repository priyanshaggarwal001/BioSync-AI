from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.services.trend_service import trend_service


class InsightService:

    def get_health_insights(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> list[dict]:

        trend_data = trend_service.get_wearable_trends(
            db,
            patient,
        )

        insights = []

        for trend in trend_data.get("trends", []):

            metric = trend["metric"]
            previous_average = trend["previous_average"]
            current_average = trend["current_average"]
            percentage_change = trend["percentage_change"]
            direction = trend["direction"]

            # -------------------------
            # Sleep
            # -------------------------

            if metric == "sleep":

                if direction == "Improving":
                    message = (
                        f"Your average sleep is improving. "
                        f"It increased from {previous_average} "
                        f"hours to {current_average} hours "
                        f"({percentage_change}% change)."
                    )

                elif direction == "Declining":
                    message = (
                        f"Your average sleep has decreased "
                        f"from {previous_average} hours to "
                        f"{current_average} hours "
                        f"({percentage_change}% change)."
                    )

                else:
                    message = (
                        f"Your average sleep remained stable "
                        f"at {current_average} hours."
                    )

            # -------------------------
            # Steps
            # -------------------------

            elif metric == "steps":

                if direction == "Improving":
                    message = (
                        f"Your activity is improving. "
                        f"Average daily steps increased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                elif direction == "Declining":
                    message = (
                        f"Your activity has decreased. "
                        f"Average daily steps went from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                else:
                    message = (
                        f"Your average daily steps remained "
                        f"stable at {current_average}."
                    )

            # -------------------------
            # Stress
            # -------------------------

            elif metric == "stress":

                if direction == "Improving":
                    message = (
                        f"Your stress level is improving. "
                        f"The average decreased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                elif direction == "Increasing":
                    message = (
                        f"Your stress level is increasing. "
                        f"The average increased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                else:
                    message = (
                        f"Your average stress level remained "
                        f"stable at {current_average}."
                    )

            # -------------------------
            # Resting Heart Rate
            # -------------------------

            elif metric == "resting_heart_rate":

                message = (
                    f"Your average resting heart rate changed "
                    f"from {previous_average} to "
                    f"{current_average} bpm "
                    f"({percentage_change}% change)."
                )

            # -------------------------
            # HRV
            # -------------------------

            elif metric == "heart_rate_variability":

                if direction == "Improving":
                    message = (
                        f"Your heart rate variability is improving. "
                        f"The average increased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                elif direction == "Declining":
                    message = (
                        f"Your heart rate variability decreased "
                        f"from {previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                else:
                    message = (
                        f"Your average heart rate variability "
                        f"remained stable at {current_average}."
                    )

            # -------------------------
            # Active Minutes
            # -------------------------

            elif metric == "active_minutes":

                if direction == "Improving":
                    message = (
                        f"Your activity duration is improving. "
                        f"Average active minutes increased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                elif direction == "Declining":
                    message = (
                        f"Your activity duration has decreased. "
                        f"Average active minutes went from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                else:
                    message = (
                        f"Your average active minutes remained "
                        f"stable at {current_average}."
                    )

            # -------------------------
            # VO2 Max
            # -------------------------

            elif metric == "vo2_max":

                if direction == "Improving":
                    message = (
                        f"Your VO₂ max is improving. "
                        f"The average increased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                elif direction == "Declining":
                    message = (
                        f"Your VO₂ max decreased from "
                        f"{previous_average} to "
                        f"{current_average} "
                        f"({percentage_change}% change)."
                    )

                else:
                    message = (
                        f"Your VO₂ max remained stable "
                        f"at {current_average}."
                    )

            else:
                continue

            insights.append(
                {
                    "metric": metric,
                    "direction": direction,
                    "percentage_change": percentage_change,
                    "message": message,
                }
            )

        return insights


insight_service = InsightService()