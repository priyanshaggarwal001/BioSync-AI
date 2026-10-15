
from app.schemas.ai_guidance import AIGuidanceResponse
from app.services.guidance_service import guidance_service


def test_guidance_response_matches_schema():
    data = guidance_service.generate_guidance({
        "trends": [
            {
                "metric": "steps",
                "previous_average": 6000,
                "current_average": 4500,
                "percentage_change": -25.0,
                "direction": "Declining",
            }
        ]
    })

    response = AIGuidanceResponse.model_validate(data)

    assert response.status == "guidance_available"
    assert len(response.guidance) == 1
    assert response.guidance[0].metric == "steps"
    assert response.guidance[0].suggestion


def test_insufficient_data_matches_schema():
    data = guidance_service.generate_guidance({"trends": []})

    response = AIGuidanceResponse.model_validate(data)

    assert response.status == "insufficient_data"
    assert response.guidance == []
