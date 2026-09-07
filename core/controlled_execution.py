"""
HOPE-AI 9F Controlled Execution

Defines a controlled execution boundary for selected tools.

This layer does not provide unrestricted system access.
Execution is permitted only when every required safety
condition is explicitly satisfied.

Current project safety configuration keeps actual execution
disabled.
"""

from core.tool_architecture import get_tool
from core.action_policy import (
    POLICY_ALLOWED,
    POLICY_DENIED,
    POLICY_HUMAN_REVIEW,
    evaluate_tool_policy,
)


LAYER = "9F"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


EXECUTION_BLOCKED = "EXECUTION_BLOCKED"
EXECUTION_NOT_ALLOWED = "EXECUTION_NOT_ALLOWED"
EXECUTION_READY = "EXECUTION_READY"


def validate_execution_request(tool_id):
    """
    Validate whether a tool is eligible to enter the
    controlled execution boundary.

    This function does not execute anything.
    """

    tool = get_tool(tool_id)

    if tool is None:
        return {
            "tool_id": tool_id,
            "decision": POLICY_DENIED,
            "execution_status": EXECUTION_BLOCKED,
            "execution_allowed": False,
            "reason": "Tool is not registered.",
        }

    policy = evaluate_tool_policy(tool)

    if policy["decision"] != POLICY_ALLOWED:
        return {
            "tool_id": tool_id,
            "decision": policy["decision"],
            "execution_status": EXECUTION_NOT_ALLOWED,
            "execution_allowed": False,
            "human_review_required": policy[
                "human_review_required"
            ],
            "reason": policy["reason"],
        }

    if not EXECUTION_ENABLED:
        return {
            "tool_id": tool_id,
            "decision": POLICY_DENIED,
            "execution_status": EXECUTION_BLOCKED,
            "execution_allowed": False,
            "human_review_required": False,
            "reason": "Global execution is disabled.",
        }

    return {
        "tool_id": tool_id,
        "decision": POLICY_ALLOWED,
        "execution_status": EXECUTION_READY,
        "execution_allowed": True,
        "human_review_required": False,
        "reason": "Tool passed the controlled execution gate.",
    }


def execute_tool(tool_id, input_data=None):
    """
    Controlled execution entry point.

    The current safety configuration intentionally prevents
    actual execution.
    """

    validation = validate_execution_request(tool_id)

    if not validation["execution_allowed"]:
        return {
            "layer": LAYER,
            "status": STATUS_READY,
            "tool_id": tool_id,
            "executed": False,
            "execution_status": validation[
                "execution_status"
            ],
            "decision": validation["decision"],
            "reason": validation["reason"],
            "input_data": input_data,
        }

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "tool_id": tool_id,
        "executed": False,
        "execution_status": EXECUTION_BLOCKED,
        "decision": POLICY_DENIED,
        "reason": (
            "Execution implementation is not enabled "
            "in the current controlled boundary."
        ),
        "input_data": input_data,
    }


def get_controlled_execution_status():
    """Return the current 9F execution boundary status."""

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "execution_enabled": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_controlled_execution_regression():
    """
    Validate the 9F controlled execution boundary.
    """

    registered_tool_result = validate_execution_request(
        "memory_store"
    )

    unknown_tool_result = validate_execution_request(
        "unknown_tool"
    )

    human_review_execution = execute_tool(
        "knowledge_lookup",
        {"query": "What is software testing?"},
    )

    status = get_controlled_execution_status()

    checks = {
        "layer_9f": LAYER == "9F",
        "status_ready": STATUS_READY == "READY",

        "registered_tool_reaches_gate": (
            registered_tool_result["tool_id"]
            == "memory_store"
        ),

        "registered_tool_not_executed": (
            registered_tool_result["execution_allowed"]
            is False
        ),

        "unknown_tool_blocked": (
            unknown_tool_result["execution_allowed"]
            is False
            and unknown_tool_result["execution_status"]
            == EXECUTION_BLOCKED
        ),

        "human_review_not_executed": (
            human_review_execution["executed"] is False
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

        "human_review_preserved": (
            human_review_execution["decision"]
            == POLICY_HUMAN_REVIEW
        ),
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "registered_tool_result": registered_tool_result,
        "unknown_tool_result": unknown_tool_result,
        "human_review_execution": human_review_execution,
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


if __name__ == "__main__":
    print("9F CONTROLLED EXECUTION REGRESSION:")
    print(get_controlled_execution_regression())
