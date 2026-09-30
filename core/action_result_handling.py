LAYER = "11G"
STATUS = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False

RESULT_SUCCESS = "SUCCESS"
RESULT_FAILED = "FAILED"
RESULT_BLOCKED = "BLOCKED"
RESULT_HUMAN_REVIEW = "HUMAN_REVIEW"

VALID_RESULTS = {
    RESULT_SUCCESS,
    RESULT_FAILED,
    RESULT_BLOCKED,
    RESULT_HUMAN_REVIEW,
}


def _normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_action_result(invocation_result):
    if not isinstance(invocation_result, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "result_valid": False,
            "result_status": RESULT_FAILED,
            "execution_allowed": False,
            "reason": "Invocation result must be a dictionary.",
        }

    if invocation_result.get("invocation_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "result_valid": False,
            "result_status": RESULT_FAILED,
            "execution_allowed": False,
            "reason": "Invocation result validation failed.",
        }

    invocation_status = _normalize_text(
        invocation_result.get("invocation_status")
    )

    if invocation_status == "BLOCKED":
        result_status = RESULT_BLOCKED
    elif invocation_status == "FAILED":
        result_status = RESULT_FAILED
    elif invocation_status == "HUMAN_REVIEW":
        result_status = RESULT_HUMAN_REVIEW
    elif invocation_status == "SUCCESS":
        result_status = RESULT_SUCCESS
    else:
        result_status = RESULT_FAILED

    execution_allowed = (
        result_status == RESULT_SUCCESS
        and invocation_result.get("execution_allowed") is True
    )

    return {
        "layer": LAYER,
        "status": STATUS,
        "result_valid": True,
        "result_status": result_status,
        "workflow_id": invocation_result.get("workflow_id"),
        "step_id": invocation_result.get("step_id"),
        "step_name": invocation_result.get("step_name"),
        "tool_id": invocation_result.get("tool_id"),
        "execution_allowed": execution_allowed,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "source_invocation_status": invocation_status,
        "reason": (
            "Action result normalized; execution remains controlled."
        ),
    }


def get_action_result_regression():
    blocked_invocation = {
        "invocation_valid": True,
        "invocation_status": "BLOCKED",
        "workflow_id": "workflow_11b_001",
        "step_id": "step_1",
        "step_name": "prepare_execution",
        "tool_id": None,
        "execution_allowed": False,
    }

    result = normalize_action_result(blocked_invocation)

    return {
        "blocked_result_valid": result["result_valid"] is True,
        "correct_layer": result["layer"] == LAYER,
        "blocked_normalized": (
            result["result_status"] == RESULT_BLOCKED
        ),
        "execution_disabled": result["execution_allowed"] is False,
        "automatic_action_disabled": (
            result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            result["decision_override_allowed"] is False
        ),
        "invalid_invocation_rejected": (
            normalize_action_result({})["result_valid"] is False
        ),
        "unknown_status_not_success": (
            normalize_action_result({
                "invocation_valid": True,
                "invocation_status": "UNKNOWN",
                "execution_allowed": True,
            })["result_status"] != RESULT_SUCCESS
        ),
    }


if __name__ == "__main__":
    regression = get_action_result_regression()

    print("HOPE 11G - Action Result Handling")
    print("-" * 45)

    for name, passed in regression.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("-" * 45)

    if all(regression.values()):
        print("11G REGRESSION: PASS")
    else:
        print("11G REGRESSION: FAIL")
