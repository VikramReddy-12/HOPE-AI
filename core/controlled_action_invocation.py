from core.controlled_execution import validate_execution_request

LAYER = "11F"
STATUS = "READY"
EXECUTION_OWNER = "9F"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def invoke_controlled_action(execution_request):
    if not isinstance(execution_request, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "invocation_valid": False,
            "invocation_status": "REJECTED",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Execution request must be a dictionary.",
        }

    if execution_request.get("request_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "invocation_valid": False,
            "invocation_status": "REJECTED",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Execution request validation failed.",
        }

    step_id = _normalize_text(execution_request.get("step_id"))
    step_name = _normalize_text(execution_request.get("step_name"))
    tool_id = _normalize_text(execution_request.get("tool_id"))

    if not step_id:
        return {
            "layer": LAYER,
            "status": STATUS,
            "invocation_valid": False,
            "invocation_status": "REJECTED",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Execution request is missing step_id.",
        }

    if not step_name:
        return {
            "layer": LAYER,
            "status": STATUS,
            "invocation_valid": False,
            "invocation_status": "REJECTED",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Execution request is missing step_name.",
        }

    if not tool_id:
        return {
            "layer": LAYER,
            "status": STATUS,
            "invocation_valid": True,
            "invocation_status": "BLOCKED",
            "workflow_id": execution_request.get("workflow_id"),
            "step_id": step_id,
            "step_name": step_name,
            "tool_id": None,
            "execution_owner": EXECUTION_OWNER,
            "gate_checked": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "No executable tool is assigned to the requested step.",
        }

    gate = validate_execution_request(tool_id)

    return {
        "layer": LAYER,
        "status": STATUS,
        "invocation_valid": True,
        "invocation_status": "BLOCKED",
        "workflow_id": execution_request.get("workflow_id"),
        "step_id": step_id,
        "step_name": step_name,
        "tool_id": tool_id,
        "execution_owner": EXECUTION_OWNER,
        "gate_checked": True,
        "gate_decision": gate.get("decision"),
        "gate_execution_status": gate.get("execution_status"),
        "gate_execution_allowed": gate.get("execution_allowed", False),
        "execution_allowed": False,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Action invocation reached the 9F controlled execution boundary; execution remains disabled.",
    }


def get_controlled_action_invocation_regression():
    valid_request = {
        "request_valid": True,
        "request_status": "PREPARED",
        "workflow_id": "workflow_11b_001",
        "step_id": "step_1",
        "step_name": "prepare_execution",
        "tool_id": None,
        "execution_owner": "9F",
        "execution_requested": True,
        "execution_allowed": False,
    }

    result = invoke_controlled_action(valid_request)

    return {
        "valid_request_invoked": result["invocation_valid"] is True,
        "correct_layer": result["layer"] == LAYER,
        "correct_owner": result["execution_owner"] == EXECUTION_OWNER,
        "invocation_blocked": result["invocation_status"] == "BLOCKED",
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
        "invalid_request_rejected": (
            invoke_controlled_action({})["invocation_valid"] is False
        ),
    }


if __name__ == "__main__":
    regression = get_controlled_action_invocation_regression()

    print("HOPE 11F - Controlled Action Invocation")
    print("-" * 50)

    for name, passed in regression.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("-" * 50)

    if all(regression.values()):
        print("11F REGRESSION: PASS")
    else:
        print("11F REGRESSION: FAIL")
