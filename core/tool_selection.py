"""
HOPE-AI 9D Tool Selection

Selects the most appropriate registered tool for capabilities
discovered from a request.

This layer only selects a tool candidate.

It does not:
- execute tools
- request permissions
- perform external actions
"""

from core.capability_discovery import discover_capabilities
from core.tool_architecture import get_tools_for_capability


LAYER = "9D"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
PERMISSION_ENABLED = False


def select_tool_for_capability(capability, request=None):
    """
    Select the most appropriate tool for a capability.

    Selection is deterministic and conservative.
    No tool is executed.
    """
    tools = get_tools_for_capability(capability)

    if not tools:
        return None

    if capability == "memory":
        normalized = ""

        if request is not None:
            normalized = str(request).strip().lower()

        if any(
            phrase in normalized
            for phrase in [
                "remember",
                "save",
                "store",
                "forget",
            ]
        ):
            preferred = "memory_store"

            if preferred in tools:
                return tools[preferred]

        preferred = "memory_recall"

        if preferred in tools:
            return tools[preferred]

    if capability == "knowledge":
        preferred = "knowledge_lookup"

        if preferred in tools:
            return tools[preferred]

    return next(iter(tools.values()))


def select_tools(request):
    """
    Discover capabilities and select one tool candidate per
    discovered capability.
    """
    discovery = discover_capabilities(request)

    selected_tools = []

    for capability in discovery["discovered_capabilities"]:
        tool = select_tool_for_capability(
            capability,
            request,
        )

        if tool is not None:
            selected_tools.append(tool)

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "request": request,
        "discovered_capabilities": discovery[
            "discovered_capabilities"
        ],
        "selected_tools": selected_tools,
        "selection_count": len(selected_tools),
        "execution_enabled": False,
        "permission_enabled": False,
    }


def get_tool_selection_status():
    """Return the current 9D selection status."""
    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "execution_enabled": EXECUTION_ENABLED,
        "permission_enabled": PERMISSION_ENABLED,
        "selection_enabled": True,
    }


def get_tool_selection_regression():
    """Validate the 9D tool selection layer."""

    memory_store_result = select_tools(
        "Remember that my favorite car is a BMW."
    )

    memory_recall_result = select_tools(
        "What is my favorite car?"
    )

    knowledge_result = select_tools(
        "What is software testing?"
    )

    unknown_result = select_tools(
        "Play some music."
    )

    status = get_tool_selection_status()

    memory_store_tools = [
        tool["tool_id"]
        for tool in memory_store_result["selected_tools"]
    ]

    memory_recall_tools = [
        tool["tool_id"]
        for tool in memory_recall_result["selected_tools"]
    ]

    knowledge_tools = [
        tool["tool_id"]
        for tool in knowledge_result["selected_tools"]
    ]

    checks = {
        "layer_9d": LAYER == "9D",
        "status_ready": STATUS_READY == "READY",

        "memory_store_selected": (
            "memory_store" in memory_store_tools
        ),

        "memory_recall_selected": (
            "memory_recall" in memory_recall_tools
        ),

        "knowledge_selected": (
            "knowledge_lookup" in knowledge_tools
        ),

        "unknown_no_tool_selected": (
            unknown_result["selected_tools"] == []
        ),

        "selection_enabled": (
            status["selection_enabled"] is True
        ),

        "execution_disabled": (
            status["execution_enabled"] is False
        ),

        "permission_disabled": (
            status["permission_enabled"] is False
        ),
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "memory_store_result": memory_store_result,
        "memory_recall_result": memory_recall_result,
        "knowledge_result": knowledge_result,
        "unknown_result": unknown_result,
        "execution_enabled": False,
        "permission_enabled": False,
    }


if __name__ == "__main__":
    print("9D TOOL SELECTION REGRESSION:")
    print(get_tool_selection_regression())
