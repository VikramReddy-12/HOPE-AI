"""
HOPE-AI 10F AI Tool Intent

Converts an AI planning result into a structured proposed tool intent.

This layer proposes tool intent only. It does not select permissions,
execute tools, modify the system, or override human/policy decisions.
"""

LAYER = "10F"
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


def create_tool_intent(request, plan=None):
    normalized_request = _normalize_request(request)

    if not normalized_request:
        return {
            "layer": LAYER,
            "status": STATUS,
            "intent_valid": False,
            "tool_intent": None,
            "reason": "A valid user request is required.",
            "execution_requested": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    if plan is not None and not isinstance(plan, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "intent_valid": False,
            "tool_intent": None,
            "reason": "Plan must be a dictionary when provided.",
            "execution_requested": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    lowered_request = normalized_request.lower()

    if any(
        keyword in lowered_request
        for keyword in (
            "remember",
            "save",
            "store",
            "memorize",
        )
    ):
        tool_id = "memory_store"
        capability = "memory"
        intent_type = "memory_save"
    elif any(
        keyword in lowered_request
        for keyword in (
            "recall",
            "remember what",
            "what did i say",
            "retrieve from memory",
        )
    ):
        tool_id = "memory_recall"
        capability = "memory"
        intent_type = "memory_recall"
    elif any(
        keyword in lowered_request
        for keyword in (
            "what is",
            "what are",
            "who is",
            "when is",
            "where is",
            "why is",
            "explain",
            "tell me about",
        )
    ):
        tool_id = "knowledge_lookup"
        capability = "knowledge"
        intent_type = "knowledge_lookup"
    else:
        tool_id = None
        capability = None
        intent_type = "no_tool_required"

    tool_intent = {
        "intent_type": intent_type,
        "tool_id": tool_id,
        "capability": capability,
        "request": normalized_request,
        "proposed_only": True,
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "request": normalized_request,
        "intent_valid": True,
        "tool_intent": tool_intent,
        "execution_requested": False,
        "execution_allowed": False,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Tool intent proposed without execution.",
    }


def get_ai_tool_intent_regression():
    memory_result = create_tool_intent(
        "Remember that my favorite car is BMW 7 Series."
    )

    knowledge_result = create_tool_intent(
        "What is artificial intelligence?"
    )

    neutral_result = create_tool_intent(
        "Hello HOPE."
    )

    invalid_result = create_tool_intent("")

    invalid_plan_result = create_tool_intent(
        "Remember this.",
        plan=[],
    )

    checks = {
        "layer_10f": LAYER == "10F",
        "status_ready": STATUS == "READY",
        "memory_intent_valid": memory_result["intent_valid"] is True,
        "memory_tool_selected": (
            memory_result["tool_intent"]["tool_id"]
            == "memory_store"
        ),
        "memory_capability_selected": (
            memory_result["tool_intent"]["capability"]
            == "memory"
        ),
        "knowledge_intent_valid": knowledge_result["intent_valid"] is True,
        "knowledge_tool_selected": (
            knowledge_result["tool_intent"]["tool_id"]
            == "knowledge_lookup"
        ),
        "knowledge_capability_selected": (
            knowledge_result["tool_intent"]["capability"]
            == "knowledge"
        ),
        "neutral_request_has_no_tool": (
            neutral_result["tool_intent"]["tool_id"]
            is None
        ),
        "invalid_request_rejected": (
            invalid_result["intent_valid"] is False
        ),
        "invalid_plan_rejected": (
            invalid_plan_result["intent_valid"] is False
        ),
        "intent_is_proposed_only": (
            memory_result["tool_intent"]["proposed_only"] is True
        ),
        "execution_not_requested": (
            memory_result["execution_requested"] is False
        ),
        "execution_disabled": (
            memory_result["execution_allowed"] is False
        ),
        "automatic_action_disabled": (
            memory_result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            memory_result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            memory_result["decision_override_allowed"] is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "memory_result": memory_result,
        "knowledge_result": knowledge_result,
        "neutral_result": neutral_result,
        "invalid_result": invalid_result,
        "invalid_plan_result": invalid_plan_result,
    }


if __name__ == "__main__":
    print("10F AI TOOL INTENT REGRESSION:")
    print(get_ai_tool_intent_regression())
