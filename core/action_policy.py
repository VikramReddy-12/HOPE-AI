"""
HOPE-AI 9E Permission / Action Policy

Defines the policy boundary for selected tools.

This layer decides whether a selected tool/action may proceed.

It does not:
- execute tools
- perform external actions
- modify HOPE
- override human authority
"""

from core.tool_selection import select_tools


LAYER = "9E"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


POLICY_ALLOWED = "ALLOWED"
POLICY_DENIED = "DENIED"
POLICY_HUMAN_REVIEW = "HUMAN_REVIEW"


def evaluate_tool_policy(tool):
    """
    Evaluate the policy for a selected tool.

    Current 9E policy is conservative:
    registered tools may be identified as candidates, but
    execution remains disabled until a later controlled layer.
    """

    if not tool:
        return {
            "decision": POLICY_DENIED,
            "reason": "No tool selected.",
            "execution_allowed": False,
            "human_review_required": False,
        }

    if not tool.get("execution_enabled", False):
        return {
            "decision": POLICY_HUMAN_REVIEW,
            "reason": "Tool execution is disabled by the current safety boundary.",
            "execution_allowed": False,
            "human_review_required": True,
        }

    if tool.get("requires_permission", False):
        return {
            "decision": POLICY_HUMAN_REVIEW,
            "reason": "Tool requires permission before execution.",
            "execution_allowed": False,
            "human_review_required": True,
        }

    return {
        "decision": POLICY_ALLOWED,
        "reason": "Tool satisfies the current policy.",
        "execution_allowed": False,
        "human_review_required": False,
    }


def evaluate_request_policy(request):
    """
    Evaluate policy for all tools selected for a request.
    """

    selection = select_tools(request)

    evaluations = []

    for tool in selection["selected_tools"]:
        policy = evaluate_tool_policy(tool)

        evaluations.append({
            "tool_id": tool["tool_id"],
            "tool_name": tool["name"],
            "capability": tool["capability"],
            "policy": policy,
        })

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "request": request,
        "selected_tools": selection["selected_tools"],
        "evaluations": evaluations,
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def get_action_policy_status():
    """Return the current 9E policy status."""

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "execution_enabled": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_action_policy_regression():
    """
    Validate the 9E permission/action policy layer.
    """

    memory_result = evaluate_request_policy(
        "Remember that my favorite car is a BMW."
    )

    knowledge_result = evaluate_request_policy(
        "What is software testing?"
    )

    unknown_result = evaluate_request_policy(
        "Play some music."
    )

    status = get_action_policy_status()

    memory_evaluations = memory_result["evaluations"]
    knowledge_evaluations = knowledge_result["evaluations"]

    checks = {
        "layer_9e": LAYER == "9E",
        "status_ready": STATUS_READY == "READY",

        "memory_tool_evaluated": (
            len(memory_evaluations) == 1
            and memory_evaluations[0]["tool_id"] == "memory_store"
        ),

        "knowledge_tool_evaluated": (
            len(knowledge_evaluations) == 1
            and knowledge_evaluations[0]["tool_id"]
            == "knowledge_lookup"
        ),

        "memory_requires_human_review": (
            len(memory_evaluations) == 1
            and memory_evaluations[0]["policy"]["decision"]
            == POLICY_HUMAN_REVIEW
        ),

        "knowledge_requires_human_review": (
            len(knowledge_evaluations) == 1
            and knowledge_evaluations[0]["policy"]["decision"]
            == POLICY_HUMAN_REVIEW
        ),

        "unknown_request_has_no_evaluations": (
            unknown_result["evaluations"] == []
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
        "memory_result": memory_result,
        "knowledge_result": knowledge_result,
        "unknown_result": unknown_result,
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


if __name__ == "__main__":
    print("9E ACTION POLICY REGRESSION:")
    print(get_action_policy_regression())
