"""
HOPE Action Dispatcher

Transitional dispatcher between R1 and the legacy Router.

Capability/action requests are prepared through the 9A-9I architecture
and the 9F controlled execution boundary.

MEMORY_SAVE, MEMORY_RECALL, and FORGET are prevented from falling through
to the legacy Router when controlled execution is blocked. Other legacy
intents remain owned by the Router during this transitional phase.
"""

from assistant.router import route
from core.capability_integration import integrate_capability_request
from core.memory_save_boundary import validate_memory_save_boundary
from memory.manager import recall


ACTION_INTENTS = {
    "MEMORY_SAVE",
    "MEMORY_RECALL",
    "FORGET",
    "KNOWLEDGE_SEARCH",
}


LAYER = "ACTION_DISPATCHER"
STATUS = "TRANSITIONAL"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _prepare_memory_save_boundary(result):
    """Prepare a MEMORY_SAVE request for the 9F boundary."""

    command = result.get("command", "")
    parts = command.split(" ", 2)

    if len(parts) == 3:
        key = parts[1]
        value = parts[2]
    else:
        key = ""
        value = ""

    return validate_memory_save_boundary(
        key,
        value,
    )


def _prepare_capability_action(result):
    """Prepare a capability action without executing it."""

    capability_result = integrate_capability_request(
        result.get("command", "")
    )

    result["action_dispatch"] = capability_result

    if result.get("intent") == "MEMORY_SAVE":
        result["action_dispatch"]["controlled_execution"] = (
            _prepare_memory_save_boundary(result)
        )

    return result


def _controlled_action_blocked_response(result):
    """Return a controlled response when execution is blocked."""

    if result.get("intent") == "MEMORY_SAVE":
        boundary = result["action_dispatch"]["controlled_execution"]

        reason = boundary.get(
            "reason",
            "Controlled execution is currently disabled.",
        )
    else:
        action_results = result["action_dispatch"].get(
            "action_results",
            [],
        )

        if action_results:
            reason = action_results[0].get(
                "reason",
                "Controlled execution is currently disabled.",
            )
        else:
            reason = "Controlled execution is currently disabled."

    return (
        "Action was not executed. "
        f"Controlled execution is blocked: {reason}"
    )


def dispatch(result):
    """Dispatch a runtime result through the appropriate execution path."""

    intent = result.get("intent", "UNKNOWN")

    if intent in ACTION_INTENTS:
        result = _prepare_capability_action(result)

        if intent == "MEMORY_SAVE":
            boundary = result["action_dispatch"].get(
                "controlled_execution",
                {},
            )

            if boundary.get("execution_allowed") is not True:
                return _controlled_action_blocked_response(result)

        else:
            action_results = result["action_dispatch"].get(
                "action_results",
                [],
            )

            if not action_results:
                return _controlled_action_blocked_response(result)

            if action_results[0].get(
                "execution_enabled"
            ) is not True:
                return _controlled_action_blocked_response(result)

    return route(result)


def get_action_dispatcher_regression():
    greeting_response = dispatch(
        {
            "intent": "GREETING",
            "command": "hello",
        }
    )

    memory_request = {
        "intent": "MEMORY_SAVE",
        "command": "remember test_cleanup hello",
    }

    prepared_result = _prepare_capability_action(memory_request)

    capability_result = prepared_result["action_dispatch"]
    boundary = capability_result["controlled_execution"]

    recall_request = {
        "intent": "MEMORY_RECALL",
        "command": "recall favorite_car",
    }

    recall_prepared = _prepare_capability_action(recall_request)

    recall_capability_result = recall_prepared["action_dispatch"]
    recall_action_results = recall_capability_result[
        "action_results"
    ]

    recall_response = dispatch(recall_request)

    forget_request = {
        "intent": "FORGET",
        "command": "forget favorite_car",
    }

    forget_before = recall("favorite_car")

    forget_prepared = _prepare_capability_action(forget_request)

    forget_capability_result = forget_prepared["action_dispatch"]
    forget_action_results = forget_capability_result[
        "action_results"
    ]

    forget_response = dispatch(forget_request)
    forget_after = recall("favorite_car")

    checks = {
        "layer": LAYER == "ACTION_DISPATCHER",
        "status": STATUS == "TRANSITIONAL",

        "dispatch_returns_string": isinstance(
            greeting_response,
            str,
        ),

        "memory_capability_result_present": (
            isinstance(capability_result, dict)
        ),

        "memory_tool_selected": any(
            tool.get("tool_id") == "memory_store"
            for tool in capability_result.get(
                "selected_tools",
                [],
            )
        ),

        "memory_boundary_present": (
            boundary["layer"] == "9F"
        ),

        "memory_execution_disabled": (
            boundary["execution_allowed"] is False
        ),

        "memory_automatic_action_disabled": (
            capability_result["automatic_action_allowed"]
            is False
        ),

        "recall_tool_selected": any(
            tool.get("tool_id") == "memory_recall"
            for tool in recall_capability_result.get(
                "selected_tools",
                [],
            )
        ),

        "recall_action_result_present": (
            len(recall_action_results) >= 1
        ),

        "recall_requires_human_review": (
            recall_action_results[0]["result_status"]
            == "HUMAN_REVIEW"
        ),

        "recall_execution_disabled": (
            recall_action_results[0]["execution_enabled"]
            is False
        ),

        "recall_response_is_string": (
            isinstance(recall_response, str)
        ),

        "forget_tool_selected": any(
            tool.get("tool_id") == "memory_forget"
            for tool in forget_capability_result.get(
                "selected_tools",
                [],
            )
        ),

        "forget_action_result_present": (
            len(forget_action_results) >= 1
        ),

        "forget_requires_human_review": (
            forget_action_results[0]["result_status"]
            == "HUMAN_REVIEW"
        ),

        "forget_execution_disabled": (
            forget_action_results[0]["execution_enabled"]
            is False
        ),

        "forget_response_is_string": (
            isinstance(forget_response, str)
        ),

        "forget_did_not_delete_memory": (
            forget_before == "BMW 7 Series"
            and forget_after == "BMW 7 Series"
        ),

        "dispatcher_execution_disabled": (
            EXECUTION_ENABLED is False
        ),

        "dispatcher_automatic_action_disabled": (
            AUTOMATIC_ACTION_ALLOWED is False
        ),

        "dispatcher_self_modification_disabled": (
            SELF_MODIFICATION_ALLOWED is False
        ),

        "dispatcher_decision_override_disabled": (
            DECISION_OVERRIDE_ALLOWED is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
    }


if __name__ == "__main__":
    print("ACTION DISPATCHER REGRESSION:")
    print(get_action_dispatcher_regression())
