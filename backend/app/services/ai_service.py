import json
from unittest import result

import httpx

from sqlalchemy.orm import Session

from app.models.patient_profiles import PatientProfile
from app.services.health_intelligence_service import (
    health_intelligence_service,
)
from app.services.trend_service import trend_service
from app.services.baseline_service import baseline_service
from app.services.insight_service import insight_service
from app.schemas.ai_summary import AISummaryContent
from app.schemas.ai_guidance import AIGuidanceResponse
from app.services.guidance_service import guidance_service

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:latest"


class AIService:

    async def generate_health_summary(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> dict:

        # --------------------------------
        # 1. Calculate wellness score
        # --------------------------------

        wellness_score = (
            health_intelligence_service.calculate_wellness_score(
                db,
                patient,
            )
        )

        # --------------------------------
        # 2. Get personal baseline
        # --------------------------------

        baseline_data = (
            baseline_service.get_wearable_baseline(
                db,
                patient,
            )
        )

        # --------------------------------
        # 3. Get trends
        # --------------------------------

        trend_data = (
            trend_service.get_wearable_trends(
                db,
                patient,
            )
        )

        # --------------------------------
        # 4. Get existing insights
        # --------------------------------

        insights = (
            insight_service.get_health_insights(
                db,
                patient,
            )
        )

        # --------------------------------
        # 5. Build structured health facts
        # --------------------------------

        verified_trends = [
            insight["message"]
            for insight in insights
        ]

        health_facts = {
            "wellness_score": wellness_score,
            "verified_trends": verified_trends,
        }

        # --------------------------------
        # 6. Convert facts to JSON
        # --------------------------------

        health_facts_json = json.dumps(
            health_facts,
            indent=2,
            default=str,
        )

        # --------------------------------
        # 7. Controlled AI prompt
        # --------------------------------

        prompt = f"""
You are the natural-language explanation layer of BioSync AI.

Your job is to rewrite the PROVIDED HEALTH FACTS into a clear,
friendly wellness summary.

The Python backend has already calculated and interpreted all
health trends.

You MUST preserve the meaning of the provided facts.

STRICT RULES:

1. Use ONLY the information provided in HEALTH FACTS.
2. Do NOT calculate anything.
3. Do NOT change any numbers.
4. Do NOT reverse a trend.
5. Do NOT reinterpret a trend.
6. Do NOT add medical conclusions.
7. Do NOT diagnose any condition.
8. Do NOT say the patient is healthy or unhealthy.
9. Do NOT use phrases such as "better cardiovascular health".
10. Do NOT describe resting heart rate as healthy, unhealthy,
    concerning, or requiring attention.
11. If the provided insight says "improving", say improving.
12. If the provided insight says "declining", say declining.
13. If the provided insight is neutral, keep it neutral.
14. Do not invent symptoms, causes, treatments, or recommendations.
15. The wellness score is a prototype wellness/recovery score.
16. Do not describe the wellness score as a medical assessment.
17. Keep the language simple and patient-friendly.
18. The output must remain informational.
21. Never describe the wellness score as evidence of overall health.
22. Never use phrases such as "strong health profile", "good health",
    "healthy", or "better health".
23. Never say that a metric improved the patient's health.
24. For resting heart rate, only describe the numerical change.
25. For stress, describe only the tracked stress-level change.
26. Do not infer causes for any metric change.
27. Describe metric changes using neutral numerical language such as increased, decreased, or remained stable.
28. Do not use "improving", "positive", "better", or "worse" unless that exact interpretation is explicitly provided in the input facts.
29. Do not make conclusions about the patient's overall health or wellness.
30. The "what_this_means" field must only summarize observable changes in the provided metrics.
31. Do not infer that a numerical change is beneficial or harmful.

IMPORTANT:

The insights in HEALTH FACTS are authoritative.
Your job is to summarize them, NOT reinterpret them.

Return ONLY valid JSON.

Use exactly this structure:

{{
  "overall_summary": "2-3 sentences describing the provided wellness score and tracked metric changes. Do not evaluate the patient's overall health.",
  "key_trends": [
    "...",
    "...",
    "..."
  ],
  "what_this_means": "2-3 sentences describing what the tracked changes show. Do not describe the patient as healthy, unhealthy, medically improved, or medically at risk.",
  "disclaimer": "This is an informational wellness summary based on tracked data and is not a medical diagnosis."
}}

HEALTH FACTS:

{health_facts_json}
"""

        # --------------------------------
        # 8. Call Ollama
        # --------------------------------

        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        async with httpx.AsyncClient(
            timeout=120.0
        ) as client:

            response = await client.post(
                OLLAMA_URL,
                json=payload,
            )

            response.raise_for_status()

            result = response.json()

        # --------------------------------
        # 9. Parse and validate AI response
        # --------------------------------

        ai_response = result.get(
            "response",
            "",
        ).strip()

        try:
            generated_json = json.loads(
                ai_response
            )

            validated_summary = AISummaryContent.model_validate(
                generated_json
            )

            ai_summary = validated_summary.model_dump()
            ai_summary["key_trends"] = verified_trends

            ai_summary["overall_summary"] = (
                f"Your current wellness score is {wellness_score}, "
                "based on your tracked wellness metrics."
            )

            ai_summary["what_this_means"] = (
                "Your tracked data shows changes across several wellness "
                "metrics when comparing the current period with the previous period. "
                "These statements describe recorded metric changes and do not "
                "establish a change in overall health."
            )

            ai_summary["disclaimer"] = (
                 "This is an informational wellness summary based on tracked data "
                 "and is not a medical diagnosis."
            )

        except (json.JSONDecodeError, ValueError):
            ai_summary = {
                "overall_summary": ai_response,
                "key_trends": [],
                "what_this_means": "",
                "disclaimer": (
                    "This is an informational wellness summary "
                    "based on tracked data and is not a medical diagnosis."
                ),
            }
        # --------------------------------
        # 10. Return response
        # --------------------------------

        return {
            "model": OLLAMA_MODEL,
            "wellness_score": wellness_score,
            "ai_summary": ai_summary,
        }
    
    
    async def generate_actionable_guidance(
        self,
        db: Session,
        patient: PatientProfile,
    ) -> dict:

        # 1. Retrieve verified wearable trends
        trend_data = trend_service.get_wearable_trends(
            db,
            patient,
        )

        # 2. Generate approved guidance using Python rules
        guidance_data = guidance_service.generate_guidance(
            trend_data,
        )

        # 3. Validate the rule-based guidance
        validated_guidance = AIGuidanceResponse.model_validate(
            guidance_data,
        )

        authoritative_guidance = validated_guidance.model_dump()

        # No need to call the LLM when there are no suggestions
        if not authoritative_guidance["guidance"]:
            return authoritative_guidance

        # 4. Give Llama only the approved guidance
        approved_guidance_json = json.dumps(
            authoritative_guidance["guidance"],
            indent=2,
        )

        
        prompt = f"""
You are the language explanation layer of BioSync AI.

Your task is to restate each approved wellness suggestion
in simple, supportive language.

STRICT RULES:
1. Use only the supplied approved guidance.
2. Do not add, remove, or change any recommendation.
3. Preserve each metric and its approved suggestion exactly
   in meaning.
4. Do not introduce physiological explanations or mechanisms.
5. Do not claim that a suggestion will improve, regulate,
   prevent, treat, or control a health metric or condition.
6. Do not diagnose, prescribe, or infer causes.
7. Do not add targets, numbers, or new actions.
8. Keep each explanation to one short sentence.
9. If you cannot explain a suggestion without adding claims,
   repeat the approved suggestion in simpler wording.
10. Return valid JSON only.

OUTPUT REQUIREMENTS:
- Return exactly one JSON object with one key: "guidance".
- "guidance" must contain exactly
  {len(authoritative_guidance["guidance"])} objects.
- Each object must contain exactly "metric" and "explanation".
- Copy each metric exactly as supplied.
- Include every approved metric exactly once.

Required format:
{{
  "guidance": [
    {{
      "metric": "sleep",
      "explanation": "A concise restatement of the approved suggestion."
    }}
  ]
}}

APPROVED GUIDANCE:
{approved_guidance_json}
"""


        payload = {
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        explanations_by_metric = {}

        # 5. Call local Ollama with a safe fallback
        try:
            async with httpx.AsyncClient(
                timeout=60.0
            ) as client:
                response = await client.post(
                    OLLAMA_URL,
                    json=payload,
                )
                response.raise_for_status()

                ollama_result = response.json()
                ai_response = ollama_result.get(
                    "response",
                    "",
                ).strip()

            generated_json = json.loads(ai_response)

            generated_items = generated_json.get("guidance")

            if not isinstance(generated_items, list):
                raise ValueError("Invalid guidance structure")

            expected_metrics = [
                item["metric"]
                for item in authoritative_guidance["guidance"]
            ]

            for item in generated_items:
                if not isinstance(item, dict):
                    raise ValueError("Invalid guidance item")

                metric = item.get("metric")
                explanation = item.get("explanation")

                if (
                    metric not in expected_metrics
                    or not isinstance(explanation, str)
                    or not explanation.strip()
                    or metric in explanations_by_metric
                ):
                    raise ValueError("Invalid guidance explanation")

                explanations_by_metric[metric] = explanation.strip()

            if set(explanations_by_metric) != set(expected_metrics):
                raise ValueError("Missing guidance explanations")

        except (
            httpx.HTTPError,
            json.JSONDecodeError,
            ValueError,
            TypeError,
            AttributeError,
            KeyError,
        ) as exc:
            print(
                f"[AI GUIDANCE ERROR] "
                f"{type(exc).__name__}: {exc}"
            )

            # Preserve rule-based guidance when Ollama fails
            explanations_by_metric = {}

        # 6. Preserve Python's authoritative observations and suggestions
        for item in authoritative_guidance["guidance"]:
            item["ai_explanation"] = explanations_by_metric.get(
                item["metric"],
                item["suggestion"],
            )

        authoritative_guidance["ai_model"] = OLLAMA_MODEL
        authoritative_guidance["ai_explanation_status"] = (
            "generated"
            if explanations_by_metric
            else "fallback"
        )

        return AIGuidanceResponse.model_validate(
             authoritative_guidance
        ).model_dump()




ai_service = AIService()