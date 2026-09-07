"""
HOPE-AI 9B Capability Discovery

Discovers which registered capabilities are relevant to a request.

This layer only discovers capabilities.
It does not select tools.
It does not request permissions.
It does not execute actions.
"""

from core.capabilities import get_capabilities


LAYER = "9B"
STATUS_READY = "READY"


def _normalize_request(request):
    """Normalize a request for capability discovery."""
    if request is None:
        return ""

    return str(request).strip().lower()


def discover_capabilities(request):
    """
    Discover capabilities relevant to the supplied request.

    Discovery is intentionally conservative. It identifies registered
    capabilities from simple request signals without executing anything.
    """
    normalized = _normalize_request(request)
    capabilities = get_capabilities()

    discovered = []

    keyword_map = {
        "memory": [
            "remember",
            "recall",
            "forget",
            "favorite",
            "save this",
            "store this",
        ],
        "knowledge": [
            "what is",
            "what are",
            "who is",
            "when is",
            "where is",
            "why is",
            "explain",
            "tell me about",
        ],
        "conversation": [
            "conversation",
            "previous message",
            "earlier",
            "context",
            "what did i say",
        ],
        "reasoning": [
            "reason",
            "analyze",
            "analysis",
            "compare",
            "why",
            "evaluate",
        ],
        "goals": [
            "goal",
            "objective",
            "target",
            "progress",
        ],
        "planning": [
            "plan",
            "planning",
            "roadmap",
            "steps",
            "schedule",
        ],
        "adaptive_intelligence": [
            "adapt",
            "adaptive",
            "personalize",
            "adjust strategy",
        ],
    }

    for capability_name, keywords in keyword_map.items():
        if capability_name not in capabilities:
            continue

        if any(keyword in normalized for keyword in keywords):
            discovered.append(capability_name)

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "request": request,
        "normalized_request": normalized,
        "discovered_capabilities": discovered,
        "discovery_count": len(discovered),
        "execution_enabled": False,
    }


def get_capability_discovery_status():
    """Return the current 9B discovery status."""
    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "execution_enabled": False,
        "tool_selection_enabled": False,
        "permission_request_enabled": False,
    }


def get_capability_discovery_regression():
    """Validate the 9B capability discovery layer."""
    memory_result = discover_capabilities(
        "Remember that my favorite car is a BMW."
    )

    knowledge_result = discover_capabilities(
        "What is software testing?"
    )

    planning_result = discover_capabilities(
        "Create a roadmap for learning Python."
    )

    unknown_result = discover_capabilities(
        "Play some music."
    )

    status = get_capability_discovery_status()

    checks = {
        "layer_9b": LAYER == "9B",
        "status_ready": STATUS_READY == "READY",
        "memory_discovered": (
            "memory"
            in memory_result["discovered_capabilities"]
        ),
        "knowledge_discovered": (
            "knowledge"
            in knowledge_result["discovered_capabilities"]
        ),
        "planning_discovered": (
            "planning"
            in planning_result["discovered_capabilities"]
        ),
        "unknown_not_invented": (
            "voice"
            not in unknown_result["discovered_capabilities"]
        ),
        "execution_disabled": (
            status["execution_enabled"] is False
        ),
        "tool_selection_disabled": (
            status["tool_selection_enabled"] is False
        ),
        "permission_disabled": (
            status["permission_request_enabled"] is False
        ),
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "memory_result": memory_result,
        "knowledge_result": knowledge_result,
        "planning_result": planning_result,
        "unknown_result": unknown_result,
        "execution_enabled": False,
    }


if __name__ == "__main__":
    print("9B CAPABILITY DISCOVERY REGRESSION:")
    print(get_capability_discovery_regression())
