"""
HOPE-AI 10C AI Model Selection

Selects an appropriate registered AI model for a request.

This layer only evaluates model suitability.
It does not call models, execute tools, modify the system,
or override human/policy decisions.
"""

from core.ai_model_registry import get_model_registry


LAYER = "10C"
STATUS = "READY"

AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_request(request):
    if not isinstance(request, str):
        return ""

    return request.strip().lower()


def _request_requirements(request):
    text = _normalize_request(request)

    return {
        "reasoning_required": any(
            word in text
            for word in (
                "reason",
                "reasoning",
                "analyze",
                "analysis",
                "evaluate",
                "compare",
            )
        ),
        "coding_required": any(
            word in text
            for word in (
                "code",
                "coding",
                "program",
                "programming",
                "python",
                "debug",
            )
        ),
        "general_assistance": True,
        "tool_use_required": any(
            word in text
            for word in (
                "tool",
                "execute",
                "action",
            )
        ),
    }


def _score_model(model, requirements):
    score = 0

    if requirements["reasoning_required"] and model.get("reasoning"):
        score += 3

    if requirements["coding_required"] and model.get("coding"):
        score += 3

    if requirements["general_assistance"] and model.get(
        "general_assistance"
    ):
        score += 1

    if requirements["tool_use_required"] and model.get("tool_use"):
        score += 2

    return score


def select_model(request):
    requirements = _request_requirements(request)
    registry = get_model_registry()

    candidates = []

    for provider, provider_data in registry.items():
        if not provider_data.get("configured"):
            continue

        for model_id, model in provider_data.get("models", {}).items():
            if model.get("availability") != "registered":
                continue

            score = _score_model(model, requirements)

            candidates.append(
                {
                    "provider": provider,
                    "model_id": model_id,
                    "display_name": model.get("display_name"),
                    "score": score,
                    "requirements": dict(requirements),
                }
            )

    candidates.sort(
        key=lambda candidate: candidate["score"],
        reverse=True,
    )

    if not candidates:
        return {
            "layer": LAYER,
            "status": STATUS,
            "request": request,
            "requirements": requirements,
            "selected_model": None,
            "candidates": [],
            "selection_available": False,
            "reason": "No configured registered model is available.",
        }

    selected = candidates[0]

    return {
        "layer": LAYER,
        "status": STATUS,
        "request": request,
        "requirements": requirements,
        "selected_model": selected,
        "candidates": candidates,
        "selection_available": True,
        "reason": "Best registered configured model selected.",
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_model_selection_regression():
    result = select_model(
        "Analyze and compare the HOPE architecture."
    )

    checks = {
        "layer_10c": LAYER == "10C",
        "status_ready": STATUS == "READY",
        "selection_result_present": isinstance(result, dict),
        "requirements_present": "requirements" in result,
        "candidates_present": "candidates" in result,
        "automatic_action_disabled": (
            AUTOMATIC_ACTION_ALLOWED is False
        ),
        "self_modification_disabled": (
            SELF_MODIFICATION_ALLOWED is False
        ),
        "decision_override_disabled": (
            DECISION_OVERRIDE_ALLOWED is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "selection_result": result,
    }


if __name__ == "__main__":
    print("10C AI MODEL SELECTION REGRESSION:")
    print(get_model_selection_regression())
