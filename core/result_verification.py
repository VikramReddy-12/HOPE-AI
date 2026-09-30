LAYER = "11H"
STATUS = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False

VALID_RESULT_STATUSES = {
    "SUCCESS",
    "FAILED",
    "BLOCKED",
    "HUMAN_REVIEW",
}


def _normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def verify_action_result(action_result, expected_step=None):
    if not isinstance(action_result, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_status": "REJECTED",
            "verified": False,
            "execution_allowed": False,
            "reason": "Action result must be a dictionary.",
        }

    if action_result.get("result_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_status": "REJECTED",
            "verified": False,
            "execution_allowed": False,
            "reason": "Action result validation failed.",
        }

    result_status = _normalize_text(
        action_result.get("result_status")
    )

    if result_status not in VALID_RESULT_STATUSES:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_status": "REJECTED",
            "verified": False,
            "execution_allowed": False,
            "reason": "Unknown action result status.",
        }

    if expected_step is not None:
        if not isinstance(expected_step, dict):
            return {
                "layer": LAYER,
                "status": STATUS,
                "verification_valid": False,
                "verification_status": "REJECTED",
                "verified": False,
                "execution_allowed": False,
                "reason": "Expected workflow step must be a dictionary.",
            }

        expected_step_id = _normalize_text(
            expected_step.get("step_id")
        )
        expected_tool_id = _normalize_text(
            expected_step.get("tool_id")
        )

        actual_step_id = _normalize_text(
            action_result.get("step_id")
        )
        actual_tool_id = _normalize_text(
            action_result.get("tool_id")
        )

        if expected_step_id and actual_step_id != expected_step_id:
            return {
                "layer": LAYER,
                "status": STATUS,
                "verification_valid": False,
                "verification_status": "REJECTED",
                "verified": False,
                "execution_allowed": False,
                "reason": "Action result step_id does not match expected step.",
            }

        if expected_tool_id and actual_tool_id != expected_tool_id:
            return {
                "layer": LAYER,
                "status": STATUS,
                "verification_valid": False,
                "verification_status": "REJECTED",
                "verified": False,
                "execution_allowed": False,
                "reason": "Action result tool_id does not match expected tool.",
            }

    execution_allowed = (
        action_result.get("execution_allowed") is True
    )

    if result_status == "SUCCESS" and not execution_allowed:
        return {
            "layer": LAYER,
            "status": STATUS,
            "verification_valid": False,
            "verification_status": "REJECTED",
            "verified": False,
            "execution_allowed": False,
            "reason": "SUCCESS cannot be verified when execution was not allowed.",
        }

    verified = result_status in {
        "SUCCESS",
        "FAILED",
        "BLOCKED",
        "HUMAN_REVIEW",
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "verification_valid": True,
        "verification_status": "VERIFIED",
        "verified": verified,
        "result_status": result_status,
        "workflow_id": action_result.get("workflow_id"),
        "step_id": action_result.get("step_id"),
        "step_name": action_result.get("step_name"),
        "tool_id": action_result.get("tool_id"),
        "execution_allowed": execution_allowed,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Action result passed structural and execution-truth verification.",
    }


def get_result_verification_regression():
    blocked_result = {
        "result_valid": True,
        "result_status": "BLOCKED",
        "workflow_id": "workflow_11b_001",
        "step_id": "step_1",
        "step_name": "prepare_execution",
        "tool_id": None,
        "execution_allowed": False,
    }

    result = verify_action_result(
        blocked_result,
        {
            "step_id": "step_1",
            "tool_id": None,
        },
    )

    false_success = verify_action_result({
        "result_valid": True,
        "result_status": "SUCCESS",
        "step_id": "step_1",
        "execution_allowed": False,
    })

    mismatch = verify_action_result(
        blocked_result,
        {
            "step_id": "step_2",
            "tool_id": None,
        },
    )

    return {
        "blocked_result_verified": result["verified"] is True,
        "correct_layer": result["layer"] == LAYER,
        "verification_passed": (
            result["verification_status"] == "VERIFIED"
        ),
        "false_success_rejected": (
            false_success["verified"] is False
        ),
        "step_mismatch_rejected": (
            mismatch["verified"] is False
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
        "invalid_result_rejected": (
            verify_action_result({})["verification_valid"] is False
        ),
    }


if __name__ == "__main__":
    regression = get_result_verification_regression()

    print("HOPE 11H - Result Verification")
    print("-" * 45)

    for name, passed in regression.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("-" * 45)

    if all(regression.values()):
        print("11H REGRESSION: PASS")
    else:
        print("11H REGRESSION: FAIL")
