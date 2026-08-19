"""
HOPE AI — 7E Cross-Engine Intelligence

Provides controlled information flow between registered
intelligence engines using the shared 7D OrchestrationContext.

7E responsibilities:
    - Define engine-to-engine dependencies
    - Prepare downstream engine inputs
    - Consume upstream engine outputs
    - Record cross-engine relationships
    - Validate dependency availability
    - Preserve traceability
    - Preserve advisory-only safety

This module does NOT execute engines.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from core.orchestration_context import (
    OrchestrationContext,
    validate_context,
)


CROSS_ENGINE_VERSION = "7E"

STATUS_READY = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"
EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False


@dataclass(frozen=True)
class EngineDependency:
    """
    Defines an information dependency between two engines.
    """

    upstream_engine: str
    downstream_engine: str
    required_outputs: tuple[str, ...] = ()
    stage: str = ""


@dataclass
class CrossEngineResult:
    """
    Result of a cross-engine intelligence operation.
    """

    trace_id: str
    status: str
    upstream_engine: str
    downstream_engine: str
    available_context: Dict[str, Any]
    missing_context: List[str] = field(
        default_factory=list
    )
    safety: Dict[str, Any] = field(
        default_factory=lambda: {
            "level": SAFETY_LEVEL,
            "execution_allowed": False,
            "automatic_action_allowed": False,
        }
    )


# ============================================================
# DEPENDENCY REGISTRY
# ============================================================

_ENGINE_DEPENDENCIES = (
    EngineDependency(
        upstream_engine="reasoning",
        downstream_engine="predictive",
        required_outputs=("result",),
        stage="PREDICT",
    ),
)


# ============================================================
# NORMALIZATION
# ============================================================

def _normalize_engine_id(
    engine_id: str,
) -> str:
    return (
        str(engine_id)
        .strip()
        .lower()
        .replace(" ", "_")
    )


# ============================================================
# DEPENDENCY DISCOVERY
# ============================================================

def get_engine_dependencies() -> List[EngineDependency]:
    """
    Return all registered cross-engine dependencies.
    """

    return list(
        _ENGINE_DEPENDENCIES
    )


def get_dependencies_for_engine(
    downstream_engine: str,
) -> List[EngineDependency]:
    """
    Return dependencies required by a downstream engine.
    """

    normalized = _normalize_engine_id(
        downstream_engine
    )

    return [
        dependency
        for dependency in _ENGINE_DEPENDENCIES
        if dependency.downstream_engine
        == normalized
    ]


# ============================================================
# CONTEXT EXTRACTION
# ============================================================

def get_upstream_context(
    context: OrchestrationContext,
    upstream_engine: str,
) -> Dict[str, Any]:
    """
    Retrieve information produced by an upstream engine.
    """

    engine_id = _normalize_engine_id(
        upstream_engine
    )

    output = context.get_engine_output(
        engine_id
    )

    if isinstance(
        output,
        dict,
    ):
        return dict(
            output
        )

    if output is None:
        return {}

    return {
        "value": output
    }


# ============================================================
# DEPENDENCY VALIDATION
# ============================================================

def validate_dependency(
    context: OrchestrationContext,
    dependency: EngineDependency,
) -> Dict[str, Any]:
    """
    Validate whether the upstream engine has supplied
    the information required by the downstream engine.
    """

    upstream_output = get_upstream_context(
        context,
        dependency.upstream_engine,
    )

    missing: List[str] = []

    for required in dependency.required_outputs:
        if required not in upstream_output:
            missing.append(
                required
            )

    return {
        "valid": not missing,
        "upstream_engine":
            dependency.upstream_engine,
        "downstream_engine":
            dependency.downstream_engine,
        "required_outputs":
            list(
                dependency.required_outputs
            ),
        "available_outputs":
            list(
                upstream_output.keys()
            ),
        "missing_outputs": missing,
    }


# ============================================================
# DOWNSTREAM INPUT PREPARATION
# ============================================================

def prepare_downstream_input(
    context: OrchestrationContext,
    downstream_engine: str,
) -> Dict[str, Any]:
    """
    Prepare a deterministic input package for a downstream
    engine using information already available in context.
    """

    dependencies = get_dependencies_for_engine(
        downstream_engine
    )

    input_context: Dict[str, Any] = {
        "trace_id": context.trace_id,
        "source_context_version": context.version,
        "upstream": {},
    }

    for dependency in dependencies:
        upstream = dependency.upstream_engine

        input_context["upstream"][
            upstream
        ] = get_upstream_context(
            context,
            upstream,
        )

    return input_context


# ============================================================
# CROSS-ENGINE ROUTING
# ============================================================

def route_cross_engine_context(
    context: OrchestrationContext,
    upstream_engine: str,
    downstream_engine: str,
) -> CrossEngineResult:
    """
    Transfer available upstream intelligence into the
    downstream engine context without executing either engine.
    """

    upstream = _normalize_engine_id(
        upstream_engine
    )

    downstream = _normalize_engine_id(
        downstream_engine
    )

    matching = [
        dependency
        for dependency in _ENGINE_DEPENDENCIES
        if dependency.upstream_engine == upstream
        and dependency.downstream_engine == downstream
    ]

    if not matching:
        return CrossEngineResult(
            trace_id=context.trace_id,
            status="NO_DEPENDENCY",
            upstream_engine=upstream,
            downstream_engine=downstream,
            available_context={},
        )

    dependency = matching[0]

    validation = validate_dependency(
        context,
        dependency,
    )

    available = get_upstream_context(
        context,
        upstream,
    )

    return CrossEngineResult(
        trace_id=context.trace_id,
        status=(
            STATUS_READY
            if validation["valid"]
            else "MISSING_CONTEXT"
        ),
        upstream_engine=upstream,
        downstream_engine=downstream,
        available_context=available,
        missing_context=validation[
            "missing_outputs"
        ],
    )


# ============================================================
# SAFETY
# ============================================================

def get_safety_state() -> Dict[str, Any]:
    """
    Return the immutable 7E safety boundary.
    """

    return {
        "level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
    }


# ============================================================
# 7E REGRESSION
# ============================================================

def get_cross_engine_regression() -> Dict[str, Any]:
    """
    Validate the independent 7E cross-engine layer.
    """

    context = OrchestrationContext(
        trace_id="7E-REGRESSION",
        command="cross engine regression",
        intent="TEST",
        requested_capabilities=[
            "reasoning",
            "predictive_risk",
        ],
        selected_engines=[
            "reasoning",
            "predictive",
        ],
        pipeline=[
            "UNDERSTAND",
            "GATHER",
            "REASON",
            "PLAN",
            "PREDICT",
            "VALIDATE",
            "RESPOND",
        ],
    )

    context.update_reasoning(
        {
            "result": "reasoning complete",
        }
    )

    context.set_engine_output(
        "reasoning",
        "REASON",
        {
            "result": "reasoning complete",
        },
    )

    context_validation = validate_context(
        context
    )

    routing = route_cross_engine_context(
        context,
        "reasoning",
        "predictive",
    )

    downstream = prepare_downstream_input(
        context,
        "predictive",
    )

    safety = get_safety_state()

    checks = {
        "context_valid":
            context_validation["valid"],
        "dependency_found":
            bool(
                get_dependencies_for_engine(
                    "predictive"
                )
            ),
        "upstream_context_available":
            bool(
                routing.available_context
            ),
        "routing_ready":
            routing.status == STATUS_READY,
        "downstream_input_ready":
            bool(
                downstream["upstream"]
            ),
        "trace_preserved":
            routing.trace_id
            == context.trace_id,
        "execution_blocked":
            safety[
                "execution_allowed"
            ] is False,
        "automatic_action_blocked":
            safety[
                "automatic_action_allowed"
            ] is False,
    }

    return {
        "integration_layer":
            CROSS_ENGINE_VERSION,
        "integration_status":
            STATUS_READY,
        "trace_id":
            context.trace_id,
        "dependency_count":
            len(
                _ENGINE_DEPENDENCIES
            ),
        "upstream":
            routing.upstream_engine,
        "downstream":
            routing.downstream_engine,
        "status":
            routing.status,
        "safety":
            safety,
        "checks":
            checks,
        "regression_passed":
            all(
                checks.values()
            ),
    }