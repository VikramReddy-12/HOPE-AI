"""
HOPE Runtime Integration Adapter (R1)

Connects the existing Brain/Router runtime to the newer
7J orchestration and 9A-9I capability/action architecture.

R1 is an integration boundary only.

Current transitional ownership:
    Brain
        -> understands the request

    R1
        -> connects the request to the newer architecture

    7J / 8A-8N
        -> orchestration and adaptive intelligence

    9A-9I
        -> capability/action architecture

    9F
        -> controlled execution gate

    Router
        -> current legacy execution authority

R1 does NOT execute tools, modify memory, authorize actions,
or replace the existing Router.
"""

from dataclasses import asdict

from core.intelligence_orchestrator import (
    OrchestrationRequest,
    orchestrate,
)

from core.capability_discovery import discover_capabilities
from core.capability_integration import integrate_capability_request


LAYER = "R1"
STATUS = "READY"


# ============================================================
# R1 OWNERSHIP CONTRACT
# ============================================================

RUNTIME_OWNERSHIP = {
    "brain": "request_understanding",
    "r1": "runtime_integration",
    "orchestration": "7J_8A_8N",
    "capability_action_architecture": "9A_9I",
    "controlled_execution": "9F",
    "legacy_execution": "router",
}


# ============================================================
# HIGH-LEVEL CAPABILITY -> ENGINE CAPABILITY MAPPING
# ============================================================

CAPABILITY_TO_ENGINE_CAPABILITIES = {
    "knowledge": [
        "knowledge_search",
        "knowledge_retrieval",
    ],
    "memory": [
        "memory_recall",
        "memory_context",
    ],
    "conversation": [
        "conversation_context",
        "conversation_summary",
    ],
    "reasoning": [
        "reasoning",
        "comparison",
        "recommendation",
    ],
    "goals": [
        "goal_detection",
        "goal_tracking",
    ],
    "planning": [
        "planning",
        "roadmap",
    ],
}


# ============================================================
# INTENT-AWARE ORCHESTRATION OVERRIDES
# ============================================================

INTENT_TO_ORCHESTRATION_CAPABILITIES = {
    # MEMORY_SAVE is an action-oriented request.
    #
    # 7J currently has recall/context capabilities for the
    # Memory Engine, but it does not own memory storage.
    #
    # Therefore R1 must NOT translate MEMORY_SAVE into
    # memory_recall or memory_context.
    #
    # The actual memory_store tool belongs to 9A-9I.
    "MEMORY_SAVE": [],

    # MEMORY_RECALL legitimately uses the existing 7J
    # Memory Engine capabilities.
    "MEMORY_RECALL": [
        "memory_recall",
        "memory_context",
    ],

    # Knowledge lookup is already represented correctly
    # by the existing orchestration capabilities.
    "KNOWLEDGE_SEARCH": [
        "knowledge_search",
        "knowledge_retrieval",
    ],
}


# ============================================================
# CAPABILITY MAPPING
# ============================================================

def _map_capabilities_to_engine_capabilities(
    capabilities
):
    """
    Convert 9B high-level capabilities into the
    engine capabilities understood by the orchestration layer.

    This is the generic capability mapping.

    Unsupported capabilities are ignored.
    Duplicates are removed while preserving order.
    """

    mapped = []

    for capability in capabilities:
        normalized = str(capability).strip().lower()

        for engine_capability in (
            CAPABILITY_TO_ENGINE_CAPABILITIES.get(
                normalized,
                [],
            )
        ):
            if engine_capability not in mapped:
                mapped.append(engine_capability)

    return mapped


def _get_intent_aware_engine_capabilities(
    intent,
    discovered_capabilities,
):
    """
    Resolve the engine capabilities that R1 should send
    to the 7J orchestration layer.

    Intent-specific mappings take priority over the generic
    high-level capability mapping.

    This prevents action-oriented intents such as
    MEMORY_SAVE from being incorrectly represented as
    memory recall operations.

    R1 does not execute the action.
    """

    normalized_intent = (
        str(intent).strip().upper()
    )

    if normalized_intent in INTENT_TO_ORCHESTRATION_CAPABILITIES:
        return list(
            INTENT_TO_ORCHESTRATION_CAPABILITIES[
                normalized_intent
            ]
        )

    return _map_capabilities_to_engine_capabilities(
        discovered_capabilities
    )


# ============================================================
# RUNTIME ADAPTER
# ============================================================

def adapt_runtime(result):
    """
    Adapt an existing Brain result into HOPE's newer architecture.

    Input:
        {
            "intent": "...",
            "command": "..."
        }

    Output:
        Original Brain result plus structured runtime metadata.

    Important:
        This function does not execute the request.
        The existing Router remains the current legacy
        execution authority.
    """

    if not isinstance(result, dict):
        result = {}

    command = str(
        result.get("command", "")
    ).strip()

    intent = str(
        result.get("intent", "UNKNOWN")
    ).strip() or "UNKNOWN"

    # --------------------------------------------------------
    # 9B: Discover high-level capabilities
    # --------------------------------------------------------

    discovery = discover_capabilities(command)

    discovered_capabilities = discovery.get(
        "discovered_capabilities",
        [],
    )

    # --------------------------------------------------------
    # R1: Resolve intent-aware orchestration capabilities
    # --------------------------------------------------------

    engine_capabilities = (
        _get_intent_aware_engine_capabilities(
            intent,
            discovered_capabilities,
        )
    )

    # --------------------------------------------------------
    # 7J: Build orchestration request
    # --------------------------------------------------------

    orchestration_request = OrchestrationRequest(
        command=command,
        intent=intent,
        context={
            "source": "brain",
            "runtime_layer": LAYER,
        },
        requested_capabilities=engine_capabilities,
    )

    orchestration = orchestrate(
        orchestration_request
    )

    # --------------------------------------------------------
    # 9I: Capability/action integration
    # --------------------------------------------------------

    capability = integrate_capability_request(
        command
    )

    orchestration_data = asdict(
        orchestration
    )

    # --------------------------------------------------------
    # Preserve original Brain result
    # --------------------------------------------------------

    adapted = dict(result)

    adapted["runtime"] = {
        "layer": LAYER,
        "status": STATUS,

        "ownership": dict(
            RUNTIME_OWNERSHIP
        ),

        "trace_id": orchestration.trace_id,

        "orchestration_status": (
            orchestration.status
        ),

        "pipeline": list(
            orchestration.pipeline
        ),

        "selected_engines": list(
            orchestration.selected_engines
        ),

        "requested_capabilities": list(
            orchestration.request.get(
                "requested_capabilities",
                [],
            )
        ),

        "discovered_capabilities": list(
            discovered_capabilities
        ),

        "orchestration": orchestration_data,

        "capability_result": capability,

        # ----------------------------------------------------
        # Safety boundary
        # ----------------------------------------------------

        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,

        # ----------------------------------------------------
        # Transitional architecture boundary
        # ----------------------------------------------------

        "controlled_execution_owner": "9F",
        "legacy_execution_owner": "router",
        "legacy_execution_active": True,
    }

    return adapted


# ============================================================
# OWNERSHIP CONTRACT STATUS
# ============================================================

def get_runtime_ownership():
    """
    Return the explicit runtime ownership contract.
    """

    return dict(
        RUNTIME_OWNERSHIP
    )


def get_runtime_ownership_status():
    """
    Return the current R1 ownership and safety status.
    """

    return {
        "layer": LAYER,
        "status": STATUS,
        "ownership": dict(
            RUNTIME_OWNERSHIP
        ),
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "legacy_execution_owner": "router",
        "legacy_execution_active": True,
        "controlled_execution_owner": "9F",
    }


# ============================================================
# R1 REGRESSION
# ============================================================

def get_runtime_adapter_regression():
    """
    Regression test for the R1 runtime adapter.
    """

    result = adapt_runtime(
        {
            "intent": "MEMORY_SAVE",
            "command": (
                "remember that my favorite car is a BMW"
            ),
        }
    )

    runtime = result["runtime"]

    ownership = runtime["ownership"]

    checks = {
        "layer": LAYER == "R1",
        "status": STATUS == "READY",

        "trace_present": bool(
            runtime["trace_id"]
        ),

        "orchestration_present": isinstance(
            runtime["orchestration"],
            dict,
        ),

        "capability_present": isinstance(
            runtime["capability_result"],
            dict,
        ),

        "memory_save_not_mapped_to_recall": (
            "memory_recall"
            not in runtime["requested_capabilities"]
        ),

        "memory_save_not_mapped_to_context": (
            "memory_context"
            not in runtime["requested_capabilities"]
        ),

        "brain_owner_correct": (
            ownership["brain"]
            == "request_understanding"
        ),

        "r1_owner_correct": (
            ownership["r1"]
            == "runtime_integration"
        ),

        "orchestration_owner_correct": (
            ownership["orchestration"]
            == "7J_8A_8N"
        ),

        "capability_owner_correct": (
            ownership["capability_action_architecture"]
            == "9A_9I"
        ),

        "controlled_execution_owner_correct": (
            ownership["controlled_execution"]
            == "9F"
        ),

        "legacy_execution_owner_correct": (
            ownership["legacy_execution"]
            == "router"
        ),

        "legacy_execution_active": (
            runtime["legacy_execution_active"]
            is True
        ),

        "execution_disabled": (
            runtime["execution_enabled"]
            is False
        ),

        "automatic_action_disabled": (
            runtime["automatic_action_allowed"]
            is False
        ),

        "self_modification_disabled": (
            runtime["self_modification_allowed"]
            is False
        ),

        "decision_override_disabled": (
            runtime["decision_override_allowed"]
            is False
        ),
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS,
        "regression_passed": all(
            checks.values()
        ),
        "checks": checks,
        "ownership": ownership,
        "result": result,
    }


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":
    print(
        "R1 RUNTIME ADAPTER REGRESSION:"
    )

    print(
        get_runtime_adapter_regression()
    )
