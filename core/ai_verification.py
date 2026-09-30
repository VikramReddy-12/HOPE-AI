"""
HOPE-AI 10G AI Verification

Verifies a proposed AI tool intent before it reaches downstream
human/policy approval.

This layer verifies proposals only. It does not execute tools,
grant permissions, modify the system, or override human decisions.
"""

LAYER = "10G"
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


def verify_tool_intent(tool_intent_result):
    if not isinstance(tool_intent_result, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_passed": False,
            "verified_intent": None,
            "reason": "Tool intent result must be a dictionary.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    if tool_intent_result.get("intent_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_passed": False,
            "verified_intent": None,
            "reason": "Tool intent is not valid.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    tool_intent = tool_intent_result.get("tool_intent")

    if not isinstance(tool_intent, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_passed": False,
            "verified_intent": None,
            "reason": "Tool intent payload is missing or invalid.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    request = _normalize_request(tool_intent.get("request"))
    intent_type = tool_intent.get("intent_type")
    tool_id = tool_intent.get("tool_id")
    capability = tool_intent.get("capability")
    proposed_only = tool_intent.get("proposed_only")

    if not request:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_passed": False,
            "verified_intent": None,
            "reason": "Verified intent must contain a valid request.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    if proposed_only is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_passed": False,
            "verified_intent": None,
            "reason": "Tool intent must remain proposed-only.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    allowed_tool_ids = {
        "memory_store",
        "memory_recall",
        "knowledge_lookup",
    }

    if tool_id is not None and tool_id not in allowed_tool_ids:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_passed": False,
            "verified_intent": None,
            "reason": "Tool is not registered in the current capability architecture.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    verified_intent = {
        "intent_type": intent_type,
        "tool_id": tool_id,
        "capability": capability,
        "request": request,
        "verified": True,
        "proposed_only": True,
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "verification_valid": True,
        "verification_passed": True,
        "verified_intent": verified_intent,
        "reason": "Tool intent verified without execution.",
        "execution_requested": False,
        "execution_allowed": False,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_ai_verification_regression():
    valid_memory_intent = {
        "intent_valid": True,
        "tool_intent": {
            "intent_type": "memory_save",
            "tool_id": "memory_store",
            "capability": "memory",
            "request": "Remember that my favorite car is BMW 7 Series.",
            "proposed_only": True,
        },
    }

    valid_knowledge_intent = {
        "intent_valid": True,
        "tool_intent": {
            "intent_type": "knowledge_lookup",
            "tool_id": "knowledge_lookup",
            "capability": "knowledge",
            "request": "What is artificial intelligence?",
            "proposed_only": True,
        },
    }

    no_tool_intent = {
        "intent_valid": True,
        "tool_intent": {
            "intent_type": "no_tool_required",
            "tool_id": None,
            "capability": None,
            "request": "Hello HOPE.",
            "proposed_only": True,
        },
    }

    invalid_result = verify_tool_intent({})
    invalid_tool_result = verify_tool_intent({
        "intent_valid": True,
        "tool_intent": {
            "intent_type": "unknown",
            "tool_id": "unknown_tool",
            "capability": "unknown",
            "request": "Do something.",
            "proposed_only": True,
        },
    })

    non_proposed_result = verify_tool_intent({
        "intent_valid": True,
        "tool_intent": {
            "intent_type": "memory_save",
            "tool_id": "memory_store",
            "capability": "memory",
            "request": "Remember this.",
            "proposed_only": False,
        },
    })

    memory_result = verify_tool_intent(valid_memory_intent)
    knowledge_result = verify_tool_intent(valid_knowledge_intent)
    no_tool_result = verify_tool_intent(no_tool_intent)

    checks = {
        "layer_10g": LAYER == "10G",
        "status_ready": STATUS == "READY",
        "memory_verification_passed": (
            memory_result["verification_passed"] is True
        ),
        "memory_tool_verified": (
            memory_result["verified_intent"]["tool_id"]
            == "memory_store"
        ),
        "knowledge_verification_passed": (
            knowledge_result["verification_passed"] is True
        ),
        "knowledge_tool_verified": (
            knowledge_result["verified_intent"]["tool_id"]
            == "knowledge_lookup"
        ),
        "no_tool_verification_passed": (
            no_tool_result["verification_passed"] is True
        ),
        "no_tool_remains_none": (
            no_tool_result["verified_intent"]["tool_id"]
            is None
        ),
        "invalid_result_rejected": (
            invalid_result["verification_passed"] is False
        ),
        "unknown_tool_rejected": (
            invalid_tool_result["verification_passed"] is False
        ),
        "non_proposed_intent_rejected": (
            non_proposed_result["verification_passed"] is False
        ),
        "verified_intent_remains_proposed": (
            memory_result["verified_intent"]["proposed_only"] is True
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
        "no_tool_result": no_tool_result,
        "invalid_result": invalid_result,
        "invalid_tool_result": invalid_tool_result,
        "non_proposed_result": non_proposed_result,
    }


if __name__ == "__main__":
    print("10G AI VERIFICATION REGRESSION:")
    print(get_ai_verification_regression())
