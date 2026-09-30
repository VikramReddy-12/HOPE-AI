"""
HOPE-AI 10E AI Planning

Creates a structured plan from an assembled AI context package.

This layer plans only. It does not call AI models, execute tools,
modify the system, or override human/policy decisions.
"""

LAYER = "10E"
STATUS = "READY"

AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_request(request):
    if request is None:
        return ""

    if not isinstance(request, str):
        request = str(request)

    return request.strip()


def create_plan(context_package):
    if not isinstance(context_package, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "plan_valid": False,
            "plan": [],
            "reason": "Context package must be a dictionary.",
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    request = _normalize_request(
        context_package.get("context", {}).get("user_request", "")
    )

    if not request:
        return {
            "layer": LAYER,
            "status": STATUS,
            "plan_valid": False,
            "plan": [],
            "reason": "A valid user request is required for planning.",
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    plan = [
        {
            "step": 1,
            "action": "understand_request",
            "description": "Understand the user's request and required outcome.",
        },
        {
            "step": 2,
            "action": "evaluate_context",
            "description": "Evaluate the available conversation, memory, knowledge, reasoning, goal, and adaptive context.",
        },
        {
            "step": 3,
            "action": "determine_next_step",
            "description": "Determine the appropriate next step without executing it.",
        },
        {
            "step": 4,
            "action": "prepare_for_policy",
            "description": "Prepare the proposed plan for downstream policy and execution controls.",
        },
    ]

    return {
        "layer": LAYER,
        "status": STATUS,
        "request": request,
        "plan_valid": True,
        "plan": plan,
        "plan_step_count": len(plan),
        "execution_requested": False,
        "execution_allowed": False,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "AI plan prepared without execution.",
    }


def get_ai_planning_regression():
    context_package = {
        "layer": "10D",
        "status": "READY",
        "request_valid": True,
        "context": {
            "user_request": "Analyze the HOPE architecture.",
            "conversation": "Previous discussion.",
            "memory": {"project": "HOPE-AI"},
            "knowledge": {"topic": "AI architecture"},
            "reasoning": {"analysis": "Layered architecture"},
            "goals": {"goal": "Build HOPE AI"},
            "adaptive_intelligence": {"strategy": "Incremental SDLC"},
            "selected_model": {
                "provider": "openai",
                "model_id": "gpt-5.6-luna",
            },
        },
    }

    result = create_plan(context_package)
    invalid_result = create_plan({})

    checks = {
        "layer_10e": LAYER == "10E",
        "status_ready": STATUS == "READY",
        "plan_valid": result["plan_valid"] is True,
        "plan_present": isinstance(result["plan"], list),
        "plan_has_steps": result["plan_step_count"] == 4,
        "request_preserved": (
            result["request"]
            == "Analyze the HOPE architecture."
        ),
        "execution_not_requested": (
            result["execution_requested"] is False
        ),
        "execution_disabled": (
            result["execution_allowed"] is False
        ),
        "invalid_context_rejected": (
            invalid_result["plan_valid"] is False
        ),
        "automatic_action_disabled": (
            result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            result["decision_override_allowed"] is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "planning_result": result,
        "invalid_result": invalid_result,
    }


if __name__ == "__main__":
    print("10E AI PLANNING REGRESSION:")
    print(get_ai_planning_regression())
