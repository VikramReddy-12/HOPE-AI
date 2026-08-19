"""
HOPE Intelligence Orchestrator

v1.5 - Intelligence Orchestration
7B - Engine Registration & Capability Discovery

Purpose:
    Provide a safe orchestration registry for HOPE's intelligence
    engines and expose deterministic capability discovery.

Design principles:
    - v1.4 remains frozen.
    - The orchestrator coordinates; it does not replace engines.
    - Engine IDs are stable canonical identifiers.
    - Human-readable engine names remain available.
    - Capability discovery is deterministic.
    - Pipeline stages are explicitly declared.
    - Predictive recommendations remain advisory only.
    - No automatic system-changing action is authorized.
    - Every orchestration request receives a trace ID.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from uuid import uuid4


# ============================================================
# VERSION / LAYER
# ============================================================

ORCHESTRATOR_VERSION = "7B"
ORCHESTRATOR_STATUS = "READY"

TRACE_PREFIX = "7C"


# ============================================================
# PIPELINE STAGES
# ============================================================

PIPELINE_STAGES = (
    "UNDERSTAND",
    "GATHER",
    "REASON",
    "PLAN",
    "PREDICT",
    "VALIDATE",
    "RESPOND",
)


# ============================================================
# SAFETY CONTRACT
# ============================================================

SAFETY_LEVEL = "ADVISORY_ONLY"
EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False


# ============================================================
# ENGINE DEFINITION
# ============================================================

@dataclass(frozen=True)
class EngineDefinition:
    """
    Canonical definition of an intelligence engine.
    """

    engine_id: str
    name: str
    capabilities: tuple[str, ...]
    stages: tuple[str, ...]
    enabled: bool = True


_ENGINE_REGISTRY: Dict[str, EngineDefinition] = {}


# ============================================================
# ORCHESTRATION REQUEST
# ============================================================

@dataclass
class OrchestrationRequest:
    """
    Structured request submitted to the intelligence orchestrator.
    """

    command: str
    intent: str = "UNKNOWN"
    context: Dict[str, Any] = field(default_factory=dict)
    requested_capabilities: List[str] = field(default_factory=list)


# ============================================================
# ORCHESTRATION RESULT
# ============================================================

@dataclass
class OrchestrationResult:
    """
    Structured result produced by the orchestrator.
    """

    trace_id: str
    status: str
    request: Dict[str, Any]
    selected_engines: List[str]
    pipeline: List[str]
    safety: Dict[str, Any]
    result: Dict[str, Any]
    errors: List[str] = field(default_factory=list)


# ============================================================
# TRACE ID
# ============================================================

def _generate_trace_id() -> str:
    """
    Generate a unique orchestration trace ID.
    """

    return f"{TRACE_PREFIX}-{uuid4().hex[:16].upper()}"


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize_engine_id(value: str) -> str:
    """
    Normalize a canonical engine ID.
    """

    return str(value).strip().lower().replace(" ", "_")


def _normalize_capability(value: str) -> str:
    """
    Normalize a capability name.
    """

    return str(value).strip().lower().replace(" ", "_")


def _normalize_stage(value: str) -> str:
    """
    Normalize a pipeline stage.
    """

    return str(value).strip().upper()


# ============================================================
# ENGINE REGISTRATION
# ============================================================

def register_engine(
    engine_id: str,
    name: str,
    capabilities: List[str] | tuple[str, ...],
    stages: List[str] | tuple[str, ...],
    enabled: bool = True,
) -> EngineDefinition:
    """
    Register an intelligence engine.

    Parameters:
        engine_id:
            Stable canonical engine identifier.

        name:
            Human-readable engine name.

        capabilities:
            Capabilities provided by the engine.

        stages:
            Pipeline stages supported by the engine.

        enabled:
            Whether the engine is available for orchestration.

    Returns:
        EngineDefinition
    """

    normalized_id = _normalize_engine_id(engine_id)
    normalized_name = str(name).strip()

    if not normalized_id:
        raise ValueError("Engine ID cannot be empty.")

    if not normalized_name:
        raise ValueError("Engine name cannot be empty.")

    normalized_capabilities = tuple(
        _normalize_capability(item)
        for item in capabilities
        if str(item).strip()
    )

    normalized_stages = tuple(
        _normalize_stage(item)
        for item in stages
        if str(item).strip()
    )

    invalid_stages = [
        stage
        for stage in normalized_stages
        if stage not in PIPELINE_STAGES
    ]

    if invalid_stages:
        raise ValueError(
            f"Unsupported pipeline stage(s): {invalid_stages}"
        )

    definition = EngineDefinition(
        engine_id=normalized_id,
        name=normalized_name,
        capabilities=normalized_capabilities,
        stages=normalized_stages,
        enabled=bool(enabled),
    )

    _ENGINE_REGISTRY[normalized_id] = definition

    return definition


# ============================================================
# ENGINE RESOLUTION
# ============================================================

def get_engine(
    engine_id: str,
) -> Optional[EngineDefinition]:
    """
    Return an engine definition by canonical engine ID.
    """

    return _ENGINE_REGISTRY.get(
        _normalize_engine_id(engine_id)
    )


def get_engine_id(
    engine_name: str,
) -> Optional[str]:
    """
    Resolve a human-readable engine name to its canonical ID.
    """

    target = str(engine_name).strip().lower()

    for engine in _ENGINE_REGISTRY.values():
        if engine.name.lower() == target:
            return engine.engine_id

    return None


def get_engine_name(
    engine_id: str,
) -> Optional[str]:
    """
    Resolve a canonical engine ID to its human-readable name.
    """

    engine = get_engine(engine_id)

    if engine is None:
        return None

    return engine.name


# ============================================================
# ENGINE REGISTRY ACCESS
# ============================================================

def get_engine_registry() -> Dict[str, EngineDefinition]:
    """
    Return a snapshot of the registered engine definitions.
    """

    return dict(_ENGINE_REGISTRY)


def get_registered_engines() -> List[str]:
    """
    Return canonical IDs of registered engines.
    """

    return list(_ENGINE_REGISTRY.keys())


def get_registered_engine_names() -> List[str]:
    """
    Return human-readable names of registered engines.
    """

    return [
        engine.name
        for engine in _ENGINE_REGISTRY.values()
    ]


# ============================================================
# CAPABILITY DISCOVERY
# ============================================================

def get_engine_capabilities(
    engine_name: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Return engine capability metadata.

    Backward-compatible behavior:
        If a human-readable engine name is supplied,
        resolve it and return its metadata.

        A canonical engine ID is also accepted.

        With no argument, return all engines keyed by
        canonical engine ID.
    """

    if engine_name is not None:
        normalized = _normalize_engine_id(engine_name)

        engine = _ENGINE_REGISTRY.get(normalized)

        if engine is None:
            resolved_id = get_engine_id(engine_name)

            if resolved_id is not None:
                engine = _ENGINE_REGISTRY.get(resolved_id)

        if engine is None:
            return {}

        return {
            "engine_id": engine.engine_id,
            "name": engine.name,
            "capabilities": list(engine.capabilities),
            "stages": list(engine.stages),
            "enabled": engine.enabled,
        }

    return {
        engine_id: {
            "name": engine.name,
            "capabilities": list(engine.capabilities),
            "stages": list(engine.stages),
            "enabled": engine.enabled,
        }
        for engine_id, engine in _ENGINE_REGISTRY.items()
    }


def get_capability_index() -> Dict[str, List[str]]:
    """
    Return a reverse capability index.

    Example:

        {
            "reasoning": ["reasoning"],
            "predictive_risk": ["predictive"]
        }
    """

    index: Dict[str, List[str]] = {}

    for engine in _ENGINE_REGISTRY.values():
        for capability in engine.capabilities:
            index.setdefault(capability, []).append(
                engine.engine_id
            )

    return {
        capability: sorted(engine_ids)
        for capability, engine_ids in sorted(index.items())
    }


def get_stage_index() -> Dict[str, List[str]]:
    """
    Return a reverse pipeline-stage index.
    """

    index: Dict[str, List[str]] = {}

    for engine in _ENGINE_REGISTRY.values():
        for stage in engine.stages:
            index.setdefault(stage, []).append(
                engine.engine_id
            )

    return {
        stage: sorted(engine_ids)
        for stage, engine_ids in sorted(index.items())
    }


# ============================================================
# ENGINE AVAILABILITY
# ============================================================

def is_engine_available(
    engine_id: str,
) -> bool:
    """
    Return whether an engine exists and is enabled.
    """

    engine = get_engine(engine_id)

    return bool(
        engine is not None
        and engine.enabled
    )


def get_available_engines() -> List[str]:
    """
    Return canonical IDs for enabled engines.
    """

    return [
        engine.engine_id
        for engine in _ENGINE_REGISTRY.values()
        if engine.enabled
    ]


# ============================================================
# CAPABILITY VALIDATION
# ============================================================

def engine_supports_capability(
    engine_id: str,
    capability: str,
) -> bool:
    """
    Determine whether an engine supports a capability.
    """

    engine = get_engine(engine_id)

    if engine is None or not engine.enabled:
        return False

    normalized = _normalize_capability(capability)

    return normalized in engine.capabilities


def validate_engine_capabilities(
    engine_id: str,
    capabilities: List[str] | tuple[str, ...],
) -> Dict[str, Any]:
    """
    Validate whether an engine supports all requested capabilities.
    """

    engine = get_engine(engine_id)

    if engine is None:
        return {
            "valid": False,
            "engine_id": _normalize_engine_id(engine_id),
            "errors": ["Engine does not exist."],
            "missing_capabilities": list(capabilities),
        }

    if not engine.enabled:
        return {
            "valid": False,
            "engine_id": engine.engine_id,
            "errors": ["Engine is disabled."],
            "missing_capabilities": list(capabilities),
        }

    requested = [
        _normalize_capability(item)
        for item in capabilities
        if str(item).strip()
    ]

    missing = [
        capability
        for capability in requested
        if capability not in engine.capabilities
    ]

    return {
        "valid": not missing,
        "engine_id": engine.engine_id,
        "errors": (
            ["One or more capabilities are unsupported."]
            if missing
            else []
        ),
        "missing_capabilities": missing,
    }


# ============================================================
# STAGE VALIDATION
# ============================================================

def engine_supports_stage(
    engine_id: str,
    stage: str,
) -> bool:
    """
    Determine whether an engine supports a pipeline stage.
    """

    engine = get_engine(engine_id)

    if engine is None or not engine.enabled:
        return False

    return _normalize_stage(stage) in engine.stages


def validate_engine_stage(
    engine_id: str,
    stage: str,
) -> Dict[str, Any]:
    """
    Validate engine compatibility with a pipeline stage.
    """

    normalized_id = _normalize_engine_id(engine_id)
    normalized_stage = _normalize_stage(stage)

    engine = get_engine(normalized_id)

    if engine is None:
        return {
            "valid": False,
            "engine_id": normalized_id,
            "stage": normalized_stage,
            "error": "Engine does not exist.",
        }

    if not engine.enabled:
        return {
            "valid": False,
            "engine_id": normalized_id,
            "stage": normalized_stage,
            "error": "Engine is disabled.",
        }

    if normalized_stage not in PIPELINE_STAGES:
        return {
            "valid": False,
            "engine_id": normalized_id,
            "stage": normalized_stage,
            "error": "Pipeline stage does not exist.",
        }

    if normalized_stage not in engine.stages:
        return {
            "valid": False,
            "engine_id": normalized_id,
            "stage": normalized_stage,
            "error": "Engine does not support this stage.",
        }

    return {
        "valid": True,
        "engine_id": normalized_id,
        "stage": normalized_stage,
        "error": None,
    }


# ============================================================
# CAPABILITY DISCOVERY / ENGINE SELECTION
# ============================================================

def discover_engines_for_capabilities(
    capabilities: List[str] | tuple[str, ...],
) -> List[str]:
    """
    Find enabled engines capable of satisfying requested capabilities.

    Selection is deterministic and returns canonical engine IDs.
    """

    requested = {
        _normalize_capability(capability)
        for capability in capabilities
        if str(capability).strip()
    }

    if not requested:
        return []

    selected = []

    for engine in _ENGINE_REGISTRY.values():
        if not engine.enabled:
            continue

        available = set(engine.capabilities)

        if requested.intersection(available):
            selected.append(engine.engine_id)

    return selected


def discover_engines_for_stage(
    stage: str,
) -> List[str]:
    """
    Return enabled engines supporting a pipeline stage.
    """

    normalized_stage = _normalize_stage(stage)

    if normalized_stage not in PIPELINE_STAGES:
        return []

    return [
        engine.engine_id
        for engine in _ENGINE_REGISTRY.values()
        if engine.enabled
        and normalized_stage in engine.stages
    ]


def discover_engine_candidates(
    capabilities: List[str] | tuple[str, ...] = (),
    stage: Optional[str] = None,
) -> List[str]:
    """
    Discover engines matching both capabilities and stage.

    If both are provided, an engine must satisfy both conditions.
    """

    candidates = [
        engine.engine_id
        for engine in _ENGINE_REGISTRY.values()
        if engine.enabled
    ]

    if capabilities:
        requested = {
            _normalize_capability(capability)
            for capability in capabilities
            if str(capability).strip()
        }

        candidates = [
            engine_id
            for engine_id in candidates
            if requested.intersection(
                set(
                    _ENGINE_REGISTRY[engine_id].capabilities
                )
            )
        ]

    if stage is not None:
        normalized_stage = _normalize_stage(stage)

        candidates = [
            engine_id
            for engine_id in candidates
            if normalized_stage in _ENGINE_REGISTRY[
                engine_id
            ].stages
        ]

    return candidates


# ============================================================
# PIPELINE VALIDATION
# ============================================================

def validate_pipeline(
    pipeline: List[str] | tuple[str, ...],
) -> Dict[str, Any]:
    """
    Validate a proposed orchestration pipeline.
    """

    stages = [
        _normalize_stage(stage)
        for stage in pipeline
        if str(stage).strip()
    ]

    invalid = [
        stage
        for stage in stages
        if stage not in PIPELINE_STAGES
    ]

    duplicate_stages = [
        stage
        for stage in stages
        if stages.count(stage) > 1
    ]

    errors = []

    if invalid:
        errors.append(
            f"Unsupported pipeline stages: {sorted(set(invalid))}"
        )

    if duplicate_stages:
        errors.append(
            f"Duplicate pipeline stages: {sorted(set(duplicate_stages))}"
        )

    return {
        "valid": not errors,
        "pipeline": stages,
        "errors": errors,
    }


# ============================================================
# SAFETY
# ============================================================

def get_orchestration_safety() -> Dict[str, Any]:
    """
    Return the v1.5 orchestration safety contract.
    """

    return {
        "level": SAFETY_LEVEL,
        "execution_allowed": EXECUTION_ALLOWED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "reason": (
            "The Intelligence Orchestrator coordinates intelligence "
            "only. Predictive recommendations remain advisory and "
            "cannot authorize automatic system-changing actions."
        ),
    }


def validate_orchestration_safety() -> bool:
    """
    Verify the orchestration safety invariant.
    """

    return (
        EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
    )


# ============================================================
# REQUEST VALIDATION
# ============================================================

def validate_request(
    request: OrchestrationRequest,
) -> Dict[str, Any]:
    """
    Validate an orchestration request.
    """

    errors = []

    if not isinstance(request, OrchestrationRequest):
        errors.append(
            "Request must be an OrchestrationRequest instance."
        )

        return {
            "valid": False,
            "errors": errors,
        }

    if not request.command.strip():
        errors.append("Command cannot be empty.")

    if not request.intent.strip():
        errors.append("Intent cannot be empty.")

    return {
        "valid": not errors,
        "errors": errors,
    }


# ============================================================
# ORCHESTRATION
# ============================================================

def orchestrate(
    request: OrchestrationRequest,
) -> OrchestrationResult:
    """
    Execute the v1.5 orchestration foundation.

    7B performs registry-driven engine discovery and
    orchestration planning only.

    Actual engine execution will be introduced in later
    orchestration milestones.
    """

    trace_id = _generate_trace_id()

    validation = validate_request(request)

    if not validation["valid"]:
        return OrchestrationResult(
            trace_id=trace_id,
            status="INVALID",
            request={
                "command": request.command
                if isinstance(request, OrchestrationRequest)
                else "",
                "intent": request.intent
                if isinstance(request, OrchestrationRequest)
                else "UNKNOWN",
            },
            selected_engines=[],
            pipeline=[],
            safety=get_orchestration_safety(),
            result={},
            errors=validation["errors"],
        )

    requested_capabilities = request.requested_capabilities

    selected_engines = discover_engines_for_capabilities(
        requested_capabilities
    )

    pipeline_validation = validate_pipeline(
        PIPELINE_STAGES
    )

    if not pipeline_validation["valid"]:
        return OrchestrationResult(
            trace_id=trace_id,
            status="INVALID",
            request={
                "command": request.command,
                "intent": request.intent,
                "context": dict(request.context),
                "requested_capabilities": list(
                    request.requested_capabilities
                ),
            },
            selected_engines=selected_engines,
            pipeline=list(PIPELINE_STAGES),
            safety=get_orchestration_safety(),
            result={},
            errors=pipeline_validation["errors"],
        )

    return OrchestrationResult(
        trace_id=trace_id,
        status=ORCHESTRATOR_STATUS,
        request={
            "command": request.command,
            "intent": request.intent,
            "context": dict(request.context),
            "requested_capabilities": list(
                request.requested_capabilities
            ),
        },
        selected_engines=selected_engines,
        pipeline=list(PIPELINE_STAGES),
        safety=get_orchestration_safety(),
        result={
            "mode": "FOUNDATION",
            "execution": "PLANNING_ONLY",
            "message": (
                "7B registry and capability discovery are ready. "
                "Engine execution will be introduced in later "
                "orchestration milestones."
            ),
        },
        errors=[],
    )


# ============================================================
# DEFAULT ENGINE REGISTRATION
# ============================================================

def register_default_engines() -> None:
    """
    Register the current HOPE intelligence architecture.
    """

    defaults = [
        (
            "brain",
            "Brain Engine",
            ["intent_detection", "input_understanding"],
            ["UNDERSTAND"],
        ),
        (
            "knowledge",
            "Knowledge Engine",
            ["knowledge_search", "knowledge_retrieval"],
            ["GATHER"],
        ),
        (
            "memory",
            "Memory Engine",
            ["memory_recall", "memory_context"],
            ["GATHER"],
        ),
        (
            "context",
            "Context Engine",
            ["conversation_context", "conversation_summary"],
            ["UNDERSTAND", "GATHER"],
        ),
        (
            "reasoning",
            "Reasoning Engine",
            ["reasoning", "comparison", "recommendation"],
            ["REASON"],
        ),
        (
            "goal",
            "Goal Engine",
            ["goal_detection", "goal_tracking"],
            ["PLAN"],
        ),
        (
            "planner",
            "Planner Engine",
            ["planning", "roadmap"],
            ["PLAN"],
        ),
        (
            "progress",
            "Progress Engine",
            ["progress_tracking", "next_topic"],
            ["PLAN"],
        ),
        (
            "recovery",
            "Recovery Intelligence",
            ["recovery_analysis", "recovery_patterns"],
            ["VALIDATE"],
        ),
        (
            "predictive",
            "Predictive Intelligence",
            ["predictive_risk", "predictive_decision"],
            ["PREDICT", "VALIDATE"],
        ),
    ]

    for (
        engine_id,
        name,
        capabilities,
        stages,
    ) in defaults:

        if engine_id not in _ENGINE_REGISTRY:
            register_engine(
                engine_id=engine_id,
                name=name,
                capabilities=capabilities,
                stages=stages,
            )


register_default_engines()


# ============================================================
# FOUNDATION STATUS
# ============================================================

def get_orchestrator_status() -> Dict[str, Any]:
    """
    Return the current 7B orchestrator status.
    """

    return {
        "version": ORCHESTRATOR_VERSION,
        "status": ORCHESTRATOR_STATUS,
        "registered_engines": len(_ENGINE_REGISTRY),
        "available_engines": len(
            get_available_engines()
        ),
        "pipeline_stages": list(PIPELINE_STAGES),
        "capabilities": len(
            get_capability_index()
        ),
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": EXECUTION_ALLOWED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "safety_valid": validate_orchestration_safety(),
    }


def get_orchestration_trace(
    result: OrchestrationResult,
) -> Dict[str, Any]:
    """
    Convert an orchestration result into a trace-friendly structure.
    """

    return {
        "trace_id": result.trace_id,
        "status": result.status,
        "request": dict(result.request),
        "selected_engines": list(
            result.selected_engines
        ),
        "pipeline": list(result.pipeline),
        "safety": dict(result.safety),
        "result": dict(result.result),
        "errors": list(result.errors),
    }


# ============================================================
# 7B REGRESSION
# ============================================================

def get_orchestrator_regression() -> Dict[str, Any]:
    """
    Run the 7B orchestration and registry invariants.
    """

    status = get_orchestrator_status()

    reasoning_id = get_engine_id(
        "Reasoning Engine"
    )

    predictive_id = get_engine_id(
        "Predictive Intelligence"
    )

    capability_candidates = (
        discover_engines_for_capabilities(
            ["reasoning", "predictive_risk"]
        )
    )

    stage_candidates = discover_engines_for_stage(
        "PREDICT"
    )

    combined_candidates = discover_engine_candidates(
        capabilities=["predictive_risk"],
        stage="PREDICT",
    )

    request = OrchestrationRequest(
        command="test orchestration",
        intent="TEST",
        requested_capabilities=[
            "reasoning",
            "predictive_risk",
        ],
    )

    result = orchestrate(request)

    trace = get_orchestration_trace(result)

    checks = {
        "status_ready": (
            status["status"] == "READY"
        ),
        "engines_registered": (
            status["registered_engines"] == 10
        ),
        "engines_available": (
            status["available_engines"] == 10
        ),
        "canonical_reasoning_id": (
            reasoning_id == "reasoning"
        ),
        "canonical_predictive_id": (
            predictive_id == "predictive"
        ),
        "capability_discovery": (
            "reasoning" in capability_candidates
            and "predictive" in capability_candidates
        ),
        "stage_discovery": (
            "predictive" in stage_candidates
        ),
        "combined_discovery": (
            combined_candidates == ["predictive"]
        ),
        "pipeline_valid": (
            validate_pipeline(
                PIPELINE_STAGES
            )["valid"]
        ),
        "trace_generated": bool(
            trace["trace_id"]
        ),
        "orchestration_ready": (
            result.status == "READY"
        ),
        "safety_valid": (
            status["safety_valid"]
        ),
        "execution_blocked": (
            result.safety[
                "execution_allowed"
            ] is False
        ),
        "automatic_action_blocked": (
            result.safety[
                "automatic_action_allowed"
            ] is False
        ),
    }

    return {
        "integration_layer": "7B",
        "integration_status": (
            "READY"
            if all(checks.values())
            else "FAILED"
        ),
        "registered_engines": status[
            "registered_engines"
        ],
        "available_engines": status[
            "available_engines"
        ],
        "capabilities": status[
            "capabilities"
        ],
        "pipeline_stages": len(
            PIPELINE_STAGES
        ),
        "reasoning_engine_id": reasoning_id,
        "predictive_engine_id": predictive_id,
        "capability_candidates": capability_candidates,
        "stage_candidates": stage_candidates,
        "combined_candidates": combined_candidates,
        "trace_id": result.trace_id,
        "selected_engines": result.selected_engines,
        "execution_allowed": result.safety[
            "execution_allowed"
        ],
        "automatic_action_allowed": result.safety[
            "automatic_action_allowed"
        ],
        "checks": checks,
        "regression_passed": all(
            checks.values()
        ),
    }
# ============================================================
# 7C — INTELLIGENT PIPELINE ROUTING
# ============================================================

ROUTING_STAGE_ORDER = {
    "UNDERSTAND": 0,
    "GATHER": 1,
    "REASON": 2,
    "PLAN": 3,
    "PREDICT": 4,
    "VALIDATE": 5,
    "RESPOND": 6,
}


def _stage_rank(stage: str) -> int:
    """
    Return the deterministic routing order of a pipeline stage.
    """

    return ROUTING_STAGE_ORDER.get(
        _normalize_stage(stage),
        999,
    )


def _engine_stages(engine_id: str) -> List[str]:
    """
    Return the stages supported by an engine.
    """

    engine = get_engine(engine_id)

    if engine is None or not engine.enabled:
        return []

    return list(engine.stages)


def build_pipeline_for_capabilities(
    capabilities: List[str] | tuple[str, ...],
) -> Dict[str, Any]:
    """
    Build an ordered intelligence pipeline from requested
    capabilities.

    7C is routing-only.

    It discovers engines, determines their stages, orders
    those stages, and validates the resulting route.

    It does not execute any engine.
    """

    requested = [
        _normalize_capability(item)
        for item in capabilities
        if str(item).strip()
    ]

    if not requested:
        return {
            "status": "INVALID",
            "capabilities": [],
            "engines": [],
            "stages": [],
            "route": [],
            "errors": [
                "At least one capability is required."
            ],
        }

    selected_engines = discover_engines_for_capabilities(
        requested
    )

    if not selected_engines:
        return {
            "status": "UNAVAILABLE",
            "capabilities": requested,
            "engines": [],
            "stages": [],
            "route": [],
            "errors": [
                "No registered engine can satisfy the "
                "requested capabilities."
            ],
        }

    selected_stages = set()

    for engine_id in selected_engines:
        for stage in _engine_stages(engine_id):
            selected_stages.add(stage)

    ordered_stages = sorted(
        selected_stages,
        key=_stage_rank,
    )

    route = [
        {
            "stage": stage,
            "engines": [
                engine_id
                for engine_id in selected_engines
                if engine_supports_stage(
                    engine_id,
                    stage,
                )
            ],
        }
        for stage in ordered_stages
    ]

    errors = []

    for item in route:
        if not item["engines"]:
            errors.append(
                f"No engine is available for stage "
                f"{item['stage']}."
            )

    validation = validate_pipeline(
        ordered_stages
    )

    if not validation["valid"]:
        errors.extend(
            validation["errors"]
        )

    return {
        "status": (
            "READY"
            if not errors
            else "INVALID"
        ),
        "capabilities": requested,
        "engines": selected_engines,
        "stages": ordered_stages,
        "route": route,
        "errors": errors,
    }


def get_pipeline_route(
    capabilities: List[str] | tuple[str, ...],
) -> Dict[str, Any]:
    """
    Public 7C pipeline-routing interface.
    """

    return build_pipeline_for_capabilities(
        capabilities
    )


def validate_routed_pipeline(
    route: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate a 7C routed pipeline.

    Validation checks:

        - route structure
        - stage ordering
        - engine existence
        - engine availability
        - engine/stage compatibility
        - safety boundary
    """

    errors = []

    if not isinstance(route, dict):
        return {
            "valid": False,
            "errors": [
                "Route must be a dictionary."
            ],
        }

    stages = route.get(
        "stages",
        [],
    )

    engines = route.get(
        "engines",
        [],
    )

    route_items = route.get(
        "route",
        [],
    )

    pipeline_validation = validate_pipeline(
        stages
    )

    if not pipeline_validation["valid"]:
        errors.extend(
            pipeline_validation["errors"]
        )

    for engine_id in engines:
        if not is_engine_available(engine_id):
            errors.append(
                f"Engine unavailable: {engine_id}"
            )

    previous_rank = -1

    for stage in stages:
        rank = _stage_rank(stage)

        if rank < previous_rank:
            errors.append(
                "Pipeline stages are not ordered."
            )

        previous_rank = rank

    for item in route_items:
        stage = item.get(
            "stage"
        )

        stage_engines = item.get(
            "engines",
            [],
        )

        if not stage_engines:
            errors.append(
                f"Stage {stage} has no assigned engine."
            )

        for engine_id in stage_engines:
            validation = validate_engine_stage(
                engine_id,
                stage,
            )

            if not validation["valid"]:
                errors.append(
                    validation["error"]
                )

    if not validate_orchestration_safety():
        errors.append(
            "Orchestration safety contract is invalid."
        )

    return {
        "valid": not errors,
        "errors": errors,
        "execution_allowed": EXECUTION_ALLOWED,
        "automatic_action_allowed": (
            AUTOMATIC_ACTION_ALLOWED
        ),
    }


def route_orchestration_request(
    request: OrchestrationRequest,
) -> Dict[str, Any]:
    """
    Build a complete 7C route for an orchestration request.

    This function performs routing only.
    """

    validation = validate_request(
        request
    )

    trace_id = _generate_trace_id()

    if not validation["valid"]:
        return {
            "trace_id": trace_id,
            "status": "INVALID",
            "route": {},
            "safety": get_orchestration_safety(),
            "errors": validation["errors"],
        }

    route = build_pipeline_for_capabilities(
        request.requested_capabilities
    )

    route_validation = validate_routed_pipeline(
        route
    )

    return {
        "trace_id": trace_id,
        "status": (
            "READY"
            if route_validation["valid"]
            else "INVALID"
        ),
        "request": {
            "command": request.command,
            "intent": request.intent,
            "requested_capabilities": list(
                request.requested_capabilities
            ),
        },
        "route": route,
        "validation": route_validation,
        "safety": get_orchestration_safety(),
        "execution": {
            "executed": False,
            "mode": "ROUTING_ONLY",
        },
        "errors": route_validation["errors"],
    }


def get_routing_trace(
    routed_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Return a trace-friendly representation of a routed request.
    """

    return {
        "trace_id": routed_result.get(
            "trace_id"
        ),
        "status": routed_result.get(
            "status"
        ),
        "selected_engines": routed_result.get(
            "route",
            {}
        ).get(
            "engines",
            [],
        ),
        "stages": routed_result.get(
            "route",
            {}
        ).get(
            "stages",
            [],
        ),
        "execution": routed_result.get(
            "execution",
            {},
        ),
        "safety": routed_result.get(
            "safety",
            {},
        ),
    }


# ============================================================
# 7C REGRESSION
# ============================================================

def get_pipeline_routing_regression() -> Dict[str, Any]:
    """
    Run the 7C intelligent pipeline-routing regression.

    The regression verifies that:

        - 7B remains healthy
        - capability-driven routing works
        - stages are ordered
        - engines match stages
        - traces are generated
        - routing does not execute anything
        - automatic actions remain blocked
    """

    baseline = get_orchestrator_regression()

    reasoning_route = build_pipeline_for_capabilities(
        ["reasoning"]
    )

    predictive_route = build_pipeline_for_capabilities(
        ["predictive_risk"]
    )

    combined_route = build_pipeline_for_capabilities(
        [
            "reasoning",
            "predictive_risk",
        ]
    )

    request = OrchestrationRequest(
        command="test intelligent routing",
        intent="TEST",
        requested_capabilities=[
            "reasoning",
            "predictive_risk",
        ],
    )

    routed = route_orchestration_request(
        request
    )

    reasoning_validation = (
        validate_routed_pipeline(
            reasoning_route
        )
    )

    predictive_validation = (
        validate_routed_pipeline(
            predictive_route
        )
    )

    combined_validation = (
        validate_routed_pipeline(
            combined_route
        )
    )

    checks = {
        "7b_baseline": (
            baseline["regression_passed"]
        ),
        "reasoning_route_ready": (
            reasoning_route["status"]
            == "READY"
        ),
        "predictive_route_ready": (
            predictive_route["status"]
            == "READY"
        ),
        "combined_route_ready": (
            combined_route["status"]
            == "READY"
        ),
        "reasoning_validation": (
            reasoning_validation["valid"]
        ),
        "predictive_validation": (
            predictive_validation["valid"]
        ),
        "combined_validation": (
            combined_validation["valid"]
        ),
        "reasoning_stage": (
            reasoning_route["stages"]
            == ["REASON"]
        ),
        "predictive_stages": (
            predictive_route["stages"]
            == [
                "PREDICT",
                "VALIDATE",
            ]
        ),
        "combined_stage_order": (
            combined_route["stages"]
            == [
                "REASON",
                "PREDICT",
                "VALIDATE",
            ]
        ),
        "trace_generated": bool(
            routed.get(
                "trace_id"
            )
        ),
        "routing_ready": (
            routed.get(
                "status"
            )
            == "READY"
        ),
        "routing_only": (
            routed.get(
                "execution",
                {}
            ).get(
                "executed"
            )
            is False
        ),
        "execution_blocked": (
            routed.get(
                "safety",
                {}
            ).get(
                "execution_allowed"
            )
            is False
        ),
        "automatic_action_blocked": (
            routed.get(
                "safety",
                {}
            ).get(
                "automatic_action_allowed"
            )
            is False
        ),
    }

    return {
        "integration_layer": "7C",
        "integration_status": (
            "READY"
            if all(checks.values())
            else "FAILED"
        ),
        "reasoning_route": reasoning_route,
        "predictive_route": predictive_route,
        "combined_route": combined_route,
        "trace_id": routed.get(
            "trace_id"
        ),
        "selected_engines": routed.get(
            "route",
            {}
        ).get(
            "engines",
            [],
        ),
        "execution_allowed": routed.get(
            "safety",
            {}
        ).get(
            "execution_allowed",
            False,
        ),
        "automatic_action_allowed": routed.get(
            "safety",
            {}
        ).get(
            "automatic_action_allowed",
            False,
        ),
        "checks": checks,
        "regression_passed": all(
            checks.values()
        ),
    }
