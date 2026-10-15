
from app.services.guidance_service import GuidanceService


def test_declining_steps_generates_guidance():
    service = GuidanceService()

    result = service.generate_guidance({
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

    assert result["status"] == "guidance_available"
    assert len(result["guidance"]) == 1
    assert result["guidance"][0]["metric"] == "steps"


def test_missing_trends_returns_insufficient_data():
    service = GuidanceService()

    result = service.generate_guidance({"trends": []})

    assert result["status"] == "insufficient_data"
    assert result["guidance"] == []


def test_stable_steps_do_not_trigger_guidance():
    service = GuidanceService()

    result = service.generate_guidance({
        "trends": [
            {
                "metric": "steps",
                "previous_average": 6000,
                "current_average": 6100,
                "percentage_change": 1.67,
                "direction": "Stable",
            }
        ]
    })

    assert result["status"] == "no_guidance_triggered"
    assert result["guidance"] == []
