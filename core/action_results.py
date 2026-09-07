"""
HOPE-AI 9G Action Results

Standardizes results returned by the controlled execution layer.

This layer:
- normalizes execution outcomes
- preserves tool identity
- preserves policy decisions
- records success/failure/block/review state
- does not execute tools
- does not enable unrestricted actions
"""

from core.controlled_execution import (
    execute_tool,
    EXECUTION_BLOCKED,
    EXECUTION_NOT_ALLOWED,
)


LAYER = "9G"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


RESULT_SUCCESS = "SUCCESS"
RESULT_FAILED = "FAILED"
RESULT_BLOCKED = "BLOCKED"
RESULT_HUMAN_REVIEW = "HUMAN_REVIEW"


def create_action_result(
    tool_id,
    result_status,
    result=None,
    error=None,
    reason=None,
    human_review_required=False,
):
    """
    Create a normalized action result.

    No execution occurs here.
    """

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "tool_id": tool_id,
        "result_status": result_status,
        "success": result_status == RESULT_SUCCESS,
        "result": result,
        "error": error,
        "reason": reason,
        "human_review_required": human_review_required,
        "execution_enabled": False,
    }


def normalize_execution_result(execution_result):
    """
    Convert a 9F execution response into the standard 9G
    action-result structure.
    """

    tool_id = execution_result.get("tool_id")
    executed = execution_result.get("executed", False)
    decision = execution_result.get("decision")
    execution_status = execution_result.get(
        "execution_status"
    )
    reason = execution_result.get("reason")

    if executed:
        return create_action_result(
            tool_id=tool_id,
            result_status=RESULT_SUCCESS,
            result=execution_result.get("result"),
            reason=reason,
            human_review_required=False,
        )

    if decision == "HUMAN_REVIEW":
        return create_action_result(
            tool_id=tool_id,
            result_status=RESULT_HUMAN_REVIEW,
            reason=reason,
            human_review_required=True,
        )

    if execution_status == EXECUTION_BLOCKED:
        return create_action_result(
            tool_id=tool_id,
            result_status=RESULT_BLOCKED,
            reason=reason,
            human_review_required=False,
        )

    if execution_status == EXECUTION_NOT_ALLOWED:
        return create_action_result(
            tool_id=tool_id,
            result_status=RESULT_HUMAN_REVIEW,
            reason=reason,
            human_review_required=True,
        )

    return create_action_result(
        tool_id=tool_id,
        result_status=RESULT_FAILED,
        error=execution_result.get("error"),
        reason=reason,
        human_review_required=False,
    )


def get_action_result(tool_id, input_data=None):
    """
    Request a controlled execution attempt and normalize
    the resulting response.

    Actual execution remains disabled by 9F.
    """

    execution_result = execute_tool(
        tool_id,
        input_data,
    )

    return normalize_execution_result(
        execution_result
    )


def get_action_results_status():
    """Return the current 9G status."""

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "execution_enabled": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_action_results_regression():
    """
    Validate the 9G action-result layer.
    """

    human_review_result = get_action_result(
        "memory_store",
        {
            "key": "favorite_car",
            "value": "BMW 7 Series",
        },
    )

    blocked_result = get_action_result(
        "unknown_tool",
        {},
    )

    status = get_action_results_status()

    checks = {
        "layer_9g": LAYER == "9G",
        "status_ready": STATUS_READY == "READY",

        "human_review_normalized": (
            human_review_result["result_status"]
            == RESULT_HUMAN_REVIEW
        ),

        "human_review_required": (
            human_review_result["human_review_required"]
            is True
        ),

        "human_review_not_success": (
            human_review_result["success"] is False
        ),

        "blocked_normalized": (
            blocked_result["result_status"]
            == RESULT_BLOCKED
        ),

        "blocked_not_success": (
            blocked_result["success"] is False
        ),

        "tool_identity_preserved": (
            human_review_result["tool_id"]
            == "memory_store"
        ),

        "unknown_tool_identity_preserved": (
            blocked_result["tool_id"]
            == "unknown_tool"
        ),

        "execution_disabled": (
            status["execution_enabled"] is False
        ),

        "automatic_action_disabled": (
            status["automatic_action_allowed"] is False
        ),

        "self_modification_disabled": (
            status["self_modification_allowed"] is False
        ),

        "decision_override_disabled": (
            status["decision_override_allowed"] is False
        ),
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "human_review_result": human_review_result,
        "blocked_result": blocked_result,
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


if __name__ == "__main__":
    print("9G ACTION RESULTS REGRESSION:")
    print(get_action_results_regression())
