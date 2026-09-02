"""
HOPE AI — 8I Adaptive Safety

Purpose:
    Provide the final safety boundary for the v1.6 adaptive
    intelligence pipeline.

Design principles:
    - Adaptive intelligence remains advisory only.
    - No system-changing execution is authorized.
    - No automatic action is authorized.
    - No self-modification is authorized.
    - No decision override is authorized.
    - Existing trace, decision, confidence, priority, strategy,
      orchestration, learning, experience, and response data are
      preserved.
    - Safety validation is deterministic.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_SAFETY_VERSION = "8I"
ADAPTIVE_SAFETY_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False

TRACE_PREFIX = "8I"


# ============================================================
# SAFETY CONTRACT
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8I safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_safety() -> bool:
    """
    Validate the complete 8I safety contract.
    """

    safety = _build_safety()

    return (
        safety["safety_level"] == "ADVISORY_ONLY"
        and safety["execution_allowed"] is False
        and safety["automatic_action_allowed"] is False
        and safety["self_modification_allowed"] is False
        and safety["decision_override_allowed"] is False
    )


# ============================================================
# RESULT MODEL
# ============================================================

@dataclass
class AdaptiveSafetyResult:
    """
    Structured 8I adaptive safety result.
    """

    trace_id: str

    status: str

    decision: str
    confidence: str
    priority: str

    adaptation: Dict[str, Any] = field(
        default_factory=dict
    )

    strategy: Dict[str, Any] = field(
        default_factory=dict
    )

    orchestration: Dict[str, Any] = field(
        default_factory=dict
    )

    learning_signal: str = ""

    experience: Dict[str, Any] = field(
        default_factory=dict
    )

    response: str = ""

    evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contributing_engines: List[str] = field(
        default_factory=list
    )

    safety: Dict[str, Any] = field(
        default_factory=_build_safety
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "",
) -> str:
    """
    Convert a value into a safe string.
    """

    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Return a defensive dictionary copy.
    """

    if isinstance(value, dict):
        return dict(value)

    return {}


def _safe_list(
    value: Any,
) -> List[Any]:
    """
    Return a defensive list copy.
    """

    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    return []


# ============================================================
# ADAPTIVE SAFETY PROCESSING
# ============================================================

def evaluate_adaptive_safety(
    *,
    trace_id: str,
    decision: Any = "",
    confidence: Any = "",
    priority: Any = "",
    adaptation: Any = None,
    strategy: Any = None,
    orchestration: Any = None,
    learning_signal: Any = "",
    experience: Any = None,
    response: Any = "",
    evidence: Any = None,
    contributing_engines: Any = None,
) -> AdaptiveSafetyResult:
    """
    Evaluate adaptive intelligence while preserving all upstream
    information.

    8I validates safety; it does not alter the decision.
    """

    safety = _build_safety()

    errors: List[str] = []

    if not validate_adaptive_safety():
        errors.append(
            "Adaptive safety contract validation failed."
        )

    normalized_trace = _safe_string(
        trace_id,
        "8I-UNKNOWN",
    )

    result = AdaptiveSafetyResult(
        trace_id=normalized_trace,
        status=(
            "SAFE"
            if not errors
            else "UNSAFE"
        ),
        decision=_safe_string(decision),
        confidence=_safe_string(confidence),
        priority=_safe_string(priority),
        adaptation=_safe_dict(adaptation),
        strategy=_safe_dict(strategy),
        orchestration=_safe_dict(orchestration),
        learning_signal=_safe_string(learning_signal),
        experience=_safe_dict(experience),
        response=_safe_string(response),
        evidence=[
            item
            for item in _safe_list(evidence)
            if isinstance(item, dict)
        ],
        contributing_engines=[
            _safe_string(item)
            for item in _safe_list(
                contributing_engines
            )
            if _safe_string(item)
        ],
        safety=safety,
        errors=errors,
    )

    return result


# ============================================================
# STATUS
# ============================================================

def get_adaptive_safety_status() -> Dict[str, Any]:
    """
    Return the current 8I module status.
    """

    return {
        "layer": ADAPTIVE_SAFETY_VERSION,
        "status": ADAPTIVE_SAFETY_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": validate_adaptive_safety(),
    }


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_safety_regression() -> Dict[str, Any]:
    """
    Run the deterministic 8I regression suite.
    """

    result = evaluate_adaptive_safety(
        trace_id="8I-REGRESSION",
        decision="ADVISORY_DECISION",
        confidence="HIGH",
        priority="MEDIUM",
        adaptation={
            "adaptation_state": "AVAILABLE",
        },
        strategy={
            "strategy": "ADAPTIVE_ADVISORY",
        },
        orchestration={
            "orchestration_state": "READY",
        },
        learning_signal="LEARNING_SIGNAL_AVAILABLE",
        experience={
            "experience_status": "RECORDED",
        },
        response="Advisory response preserved.",
        evidence=[
            {
                "source": "regression",
                "value": "validated",
            }
        ],
        contributing_engines=[
            "Reasoning Engine",
            "Predictive Intelligence Engine",
        ],
    )

    checks = {
        "status_ready": (
            ADAPTIVE_SAFETY_STATUS == "READY"
        ),
        "layer_8i": (
            ADAPTIVE_SAFETY_VERSION == "8I"
        ),
        "trace_preserved": (
            result.trace_id == "8I-REGRESSION"
        ),
        "decision_preserved": (
            result.decision == "ADVISORY_DECISION"
        ),
        "confidence_preserved": (
            result.confidence == "HIGH"
        ),
        "priority_preserved": (
            result.priority == "MEDIUM"
        ),
        "adaptation_preserved": (
            bool(result.adaptation)
        ),
        "strategy_preserved": (
            bool(result.strategy)
        ),
        "orchestration_preserved": (
            bool(result.orchestration)
        ),
        "learning_signal_preserved": (
            result.learning_signal
            == "LEARNING_SIGNAL_AVAILABLE"
        ),
        "experience_preserved": (
            bool(result.experience)
        ),
        "response_preserved": (
            bool(result.response)
        ),
        "evidence_preserved": (
            bool(result.evidence)
        ),
        "engines_preserved": (
            bool(result.contributing_engines)
        ),
        "safety_advisory": (
            result.safety["safety_level"]
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            result.safety["execution_allowed"]
            is False
        ),
        "automatic_action_blocked": (
            result.safety[
                "automatic_action_allowed"
            ]
            is False
        ),
        "self_modification_blocked": (
            result.safety[
                "self_modification_allowed"
            ]
            is False
        ),
        "decision_override_blocked": (
            result.safety[
                "decision_override_allowed"
            ]
            is False
        ),
        "global_safety_valid": (
            validate_adaptive_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8I",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "safety": result.safety,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "checks": checks,
    }