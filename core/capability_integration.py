"""
HOPE-AI 9I Capability Integration

Integrates the 9B-9H capability/action pipeline into one
coherent result.

This layer:
- discovers capabilities
- selects tools
- evaluates action policy
- passes through controlled execution
- normalizes action results
- records audit information
- returns one integrated capability result

It does not bypass safety controls.
It does not enable unrestricted execution.
"""

from core.capability_discovery import discover_capabilities
from core.tool_selection import select_tools
from core.action_policy import evaluate_request_policy
from core.action_results import get_action_result
from core.action_audit import create_audit_record


LAYER = "9I"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def integrate_capability_request(request):
    """
    Run a request through the complete 9B-9H architecture.

    No unrestricted execution is enabled.
    """

    discovery = discover_capabilities(request)
    selection = select_tools(request)
    policy = evaluate_request_policy(request)

    action_results = []
    audit_records = []

    for tool in selection["selected_tools"]:
        action_result = get_action_result(
            tool["tool_id"],
            {
                "request": request,
                "capability": tool["capability"],
            },
        )

        audit_record = create_audit_record(
            action_result
        )

        action_results.append(action_result)
        audit_records.append(audit_record)

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "request": request,
        "discovered_capabilities": discovery[
            "discovered_capabilities"
        ],
        "selected_tools": selection["selected_tools"],
        "policy_evaluations": policy["evaluations"],
        "action_results": action_results,
        "audit_records": audit_records,
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def get_capability_integration_status():
    """Return the current 9I integration status."""

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "integration_enabled": True,
        "execution_enabled": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_capability_integration_regression():
    """
    Validate the complete 9I capability integration layer.
    """

    memory_result = integrate_capability_request(
        "Remember that my favorite car is a BMW."
    )

    knowledge_result = integrate_capability_request(
        "What is software testing?"
    )

    unknown_result = integrate_capability_request(
        "Play some music."
    )

    status = get_capability_integration_status()

    memory_tools = [
        tool["tool_id"]
        for tool in memory_result["selected_tools"]
    ]

    knowledge_tools = [
        tool["tool_id"]
        for tool in knowledge_result["selected_tools"]
    ]

    memory_results = memory_result["action_results"]
    knowledge_results = knowledge_result["action_results"]

    checks = {
        "layer_9i": LAYER == "9I",
        "status_ready": STATUS_READY == "READY",
        "integration_enabled": (
            status["integration_enabled"] is True
        ),

        "memory_capability_discovered": (
            "memory"
            in memory_result["discovered_capabilities"]
        ),

        "memory_tool_selected": (
            "memory_store" in memory_tools
        ),

        "memory_policy_evaluated": (
            len(memory_result["policy_evaluations"]) >= 1
        ),

        "memory_action_result_created": (
            len(memory_results) >= 1
        ),

        "memory_result_requires_review": (
            memory_results[0]["result_status"]
            == "HUMAN_REVIEW"
        ),

        "memory_audit_created": (
            len(memory_result["audit_records"]) >= 1
        ),

        "knowledge_capability_discovered": (
            "knowledge"
            in knowledge_result["discovered_capabilities"]
        ),

        "knowledge_tool_selected": (
            "knowledge_lookup" in knowledge_tools
        ),

        "knowledge_policy_evaluated": (
            len(knowledge_result["policy_evaluations"]) >= 1
        ),

        "knowledge_action_result_created": (
            len(knowledge_results) >= 1
        ),

        "knowledge_result_requires_review": (
            knowledge_results[0]["result_status"]
            == "HUMAN_REVIEW"
        ),

        "knowledge_audit_created": (
            len(knowledge_result["audit_records"]) >= 1
        ),

        "unknown_capability_not_invented": (
            unknown_result["discovered_capabilities"] == []
        ),

        "unknown_no_tool_selected": (
            unknown_result["selected_tools"] == []
        ),

        "unknown_no_action_result": (
            unknown_result["action_results"] == []
        ),

        "unknown_no_audit": (
            unknown_result["audit_records"] == []
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
    print("9I CAPABILITY INTEGRATION REGRESSION:")
    print(get_capability_integration_regression())
