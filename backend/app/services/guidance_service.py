
from typing import Any


class GuidanceService:
    """
    Generates deterministic, general wellness guidance from
    verified wearable trends.

    Python determines which guidance is allowed.
    The LLM must not create new recommendations.
    """

    def generate_guidance(
        self,
        trend_data: dict[str, Any],
    ) -> dict[str, Any]:

        trends = trend_data.get("trends", [])

        if not trends:
            return {
                "status": "insufficient_data",
                "guidance": [],
                "message": (
                    "There is not enough wearable trend data "
                    "to generate personalized guidance yet."
                ),
            }

        guidance = []

        # Convert verified trends into a metric lookup.
        trend_lookup = {
            trend["metric"]: trend
            for trend in trends
            if trend.get("metric")
        }

        # -----------------------------------------
        # 1. Sleep guidance
        # -----------------------------------------

        sleep = trend_lookup.get("sleep")

        if sleep:
            current_sleep = sleep.get("current_average")

            if current_sleep is not None and current_sleep < 7:
                guidance.append({
                    "metric": "sleep",
                    "category": "sleep_hygiene",
                    "observation": (
                        "Average recorded sleep is below "
                        "7 hours per night."
                    ),
                    "suggestion": (
                        "Consider maintaining a consistent "
                        "sleep and wake-up schedule."
                    ),
                    "priority": "general",
                })

        # -----------------------------------------
        # 2. Activity guidance
        # -----------------------------------------

        steps = trend_lookup.get("steps")

        if steps and steps.get("direction") == "Declining":
            guidance.append({
                "metric": "steps",
                "category": "physical_activity",
                "observation": (
                    "Average daily steps have declined "
                    "compared with the previous period."
                ),
                "suggestion": (
                    "Consider adding manageable walking "
                    "sessions to your daily routine."
                ),
                "priority": "general",
            })

        active_minutes = trend_lookup.get("active_minutes")

        if (
            active_minutes
            and active_minutes.get("direction") == "Declining"
        ):
            guidance.append({
                "metric": "active_minutes",
                "category": "physical_activity",
                "observation": (
                    "Average daily active minutes have declined "
                    "compared with the previous period."
                ),
                "suggestion": (
                    "Consider building regular movement "
                    "breaks into your day, as appropriate "
                    "for your abilities."
                ),
                "priority": "general",
            })

        # -----------------------------------------
        # 3. Stress guidance
        # -----------------------------------------

        stress = trend_lookup.get("stress")

        if stress and stress.get("direction") == "Increasing":
            guidance.append({
                "metric": "stress",
                "category": "relaxation",
                "observation": (
                    "The recorded stress level has increased "
                    "compared with the previous period."
                ),
                "suggestion": (
                    "Consider taking regular breaks and "
                    "trying a relaxation exercise, such "
                    "as slow, comfortable breathing."
                ),
                "priority": "general",
            })

        # -----------------------------------------
        # 4. HRV guidance
        # -----------------------------------------

        hrv = trend_lookup.get("heart_rate_variability")

        if hrv and hrv.get("direction") == "Declining":
            guidance.append({
                "metric": "heart_rate_variability",
                "category": "recovery_routine",
                "observation": (
                    "Recorded heart rate variability has "
                    "declined compared with the previous period."
                ),
                "suggestion": (
                    "Maintain a consistent sleep and recovery "
                    "routine, and consider the trend alongside "
                    "how you feel."
                ),
                "priority": "general",
            })

        return {
            "status": (
                "guidance_available"
                if guidance
                else "no_guidance_triggered"
            ),
            "guidance": guidance,
            "message": (
                "Suggestions are based on predefined rules "
                "and recorded wearable trends. They are "
                "general wellness guidance, not medical advice."
            ),
        }


guidance_service = GuidanceService()
