"""
HOPE Action Dispatcher

Transitional dispatcher between R1 and the legacy Router.

Capability/action requests are prepared through the 9A-9I architecture
and the 9F controlled execution boundary, while actual legacy execution
remains owned by the Router until controlled execution is explicitly enabled.
"""

from assistant.router import route
from core.capability_integration import integrate_capability_request
from core.memory_save_boundary import validate_memory_save_boundary


ACTION_INTENTS = {
    "MEMORY_SAVE",
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


def dispatch(result):
    """Dispatch a runtime result through the appropriate execution path."""

    intent = result.get("intent", "UNKNOWN")

    if intent in ACTION_INTENTS:
        result = _prepare_capability_action(result)

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
