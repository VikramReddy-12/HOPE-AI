from core.controlled_execution import validate_execution_request

LAYER = "11E"
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


def create_execution_request(control):
    if not isinstance(control, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "request_valid": False,
            "request_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Step execution control must be a dictionary.",
        }

    if control.get("control_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "request_valid": False,
            "request_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Step execution control validation failed.",
        }

    if control.get("control_status") != "BLOCKED":
        return {
            "layer": LAYER,
            "status": STATUS,
            "request_valid": False,
            "request_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Execution request requires a controlled step.",
        }

    step_id = _normalize_text(control.get("step_id"))
    name = _normalize_text(control.get("name"))
    tool_id = _normalize_text(control.get("tool_id"))

    if not step_id:
        return {
            "layer": LAYER,
            "status": STATUS,
            "request_valid": False,
            "request_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Execution request requires step_id.",
        }

    if not name:
        return {
            "layer": LAYER,
            "status": STATUS,
            "request_valid": False,
            "request_status": "REJECTED",
            "step_id": step_id,
            "execution_allowed": False,
            "reason": "Execution request requires step name.",
        }

    gate = None

    if tool_id:
        gate = validate_execution_request(tool_id)

    return {
        "layer": LAYER,
        "status": STATUS,
        "request_valid": True,
        "request_status": "PREPARED",
        "workflow_id": control.get("workflow_id"),
        "step_id": step_id,
        "step_name": name,
        "tool_id": tool_id if tool_id else None,
        "execution_owner": EXECUTION_OWNER,
        "execution_requested": True,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "gate_checked": gate is not None,
        "gate_decision": gate.get("decision") if gate else None,
        "gate_execution_status": (
            gate.get("execution_status") if gate else None
        ),
        "gate_execution_allowed": (
            gate.get("execution_allowed", False) if gate else False
        ),
        "reason": "Execution request prepared; controlled execution remains disabled.",
    }


def get_execution_request_regression():
    valid_control = {
        "control_valid": True,
        "control_status": "BLOCKED",
        "workflow_id": "workflow_11b_001",
        "step_id": "step_1",
        "name": "prepare_execution",
        "tool_id": None,
        "execution_owner": "9F",
        "execution_allowed": False,
    }

    result = create_execution_request(valid_control)

    return {
        "valid_control_prepared": result["request_valid"] is True,
        "correct_layer": result["layer"] == LAYER,
        "correct_owner": result["execution_owner"] == EXECUTION_OWNER,
        "request_prepared": result["request_status"] == "PREPARED",
        "execution_requested": result["execution_requested"] is True,
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
        "invalid_control_rejected": (
            create_execution_request({})["request_valid"] is False
        ),
    }


if __name__ == "__main__":
    regression = get_execution_request_regression()

    print("HOPE 11E - Execution Request")
    print("-" * 45)

    for name, passed in regression.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("-" * 45)

    if all(regression.values()):
        print("11E REGRESSION: PASS")
    else:
        print("11E REGRESSION: FAIL")
