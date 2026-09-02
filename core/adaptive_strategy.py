"""
HOPE AI — 8B Adaptive Strategy

Purpose:
    Convert the advisory adaptation produced by 8A into a
    structured strategy recommendation.

Design principles:
    - 8B consumes existing intelligence only.
    - Strategy remains advisory.
    - No execution is permitted.
    - No automatic action is permitted.
    - No self-modification is permitted.
    - No decision override is permitted.
    - Existing trace, decision, confidence, priority,
      evidence, engines, and learning signals are preserved.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_STRATEGY_VERSION = "8B"
ADAPTIVE_STRATEGY_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# RESULT
# ============================================================

@dataclass
class AdaptiveStrategyResult:
    """
    Structured 8B strategy recommendation.
    """

    trace_id: str
    status: str

    decision: str
    confidence: str
    priority: str

    adaptation_state: str
    strategy: str
    recommendation: str

    learning_signal: str

    evidence: List[Dict[str, Any]] = field(
        default_factory=list
    )

    contributing_engines: List[str] = field(
        default_factory=list
    )

    safety: Dict[str, Any] = field(
        default_factory=lambda: {
            "safety_level": SAFETY_LEVEL,
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
        }
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "UNKNOWN",
) -> str:
    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


def _safe_list(
    value: Any,
) -> List[Any]:
    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    return []


def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)

    return {}


# ============================================================
# SAFETY
# ============================================================

def get_adaptive_strategy_safety() -> Dict[str, Any]:
    """
    Return the immutable 8B safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_strategy_safety() -> bool:
    """
    Validate the 8B safety boundary.
    """

    safety = get_adaptive_strategy_safety()

    return (
        safety["safety_level"] == "ADVISORY_ONLY"
        and safety["execution_allowed"] is False
        and safety["automatic_action_allowed"] is False
        and safety["self_modification_allowed"] is False
        and safety["decision_override_allowed"] is False
    )


# ============================================================
# STRATEGY GENERATION
# ============================================================

def _build_strategy(
    adaptation_state: str,
    learning_signal: str,
) -> str:
    """
    Produce a conservative strategy classification.

    This does not replace the existing decision.
    """

    state = adaptation_state.upper()
    signal = learning_signal.upper()

    if state == "ADAPTATION_AVAILABLE":
        if signal == "LEARNING_SIGNAL_AVAILABLE":
            return "REFINE"

        return "MONITOR_AND_REFINE"

    if state == "INSUFFICIENT_DATA":
        return "COLLECT_MORE_EVIDENCE"

    return "MONITOR"


def _build_recommendation(
    strategy: str,
    decision: str,
) -> str:
    """
    Produce a human-readable advisory recommendation.
    """

    return (
        f"Maintain decision '{decision}' and apply strategy "
        f"'{strategy}' for future advisory evaluation."
    )


# ============================================================
# INTEGRATION
# ============================================================

def integrate_adaptive_strategy(
    adaptive_intelligence: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an 8A adaptive-intelligence result into an 8B
    advisory strategy result.

    Existing intelligence is preserved.
    """

    source = _safe_dict(adaptive_intelligence)

    trace_id = _safe_string(
        source.get("trace_id"),
        "UNKNOWN",
    )

    decision = _safe_string(
        source.get("decision"),
    )

    confidence = _safe_string(
        source.get("confidence"),
    )

    priority = _safe_string(
        source.get("priority"),
    )

    adaptation_state = _safe_string(
        source.get("adaptation_state"),
        "INSUFFICIENT_DATA",
    )

    learning_signal = _safe_string(
        source.get("learning_signal"),
        "INSUFFICIENT_DATA",
    )

    evidence = _safe_list(
        source.get("evidence")
    )

    engines = _safe_list(
        source.get("contributing_engines")
    )

    strategy = _build_strategy(
        adaptation_state,
        learning_signal,
    )

    recommendation = _build_recommendation(
        strategy,
        decision,
    )

    result = AdaptiveStrategyResult(
        trace_id=trace_id,
        status=ADAPTIVE_STRATEGY_STATUS,
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
        strategy=strategy,
        recommendation=recommendation,
        learning_signal=learning_signal,
        evidence=[
            item
            for item in evidence
            if isinstance(item, dict)
        ],
        contributing_engines=[
            _safe_string(item)
            for item in engines
            if _safe_string(item)
        ],
        safety=get_adaptive_strategy_safety(),
    )

    return {
        "layer": ADAPTIVE_STRATEGY_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "adaptation_state": result.adaptation_state,
        "strategy": result.strategy,
        "recommendation": result.recommendation,
        "learning_signal": result.learning_signal,
        "evidence": result.evidence,
        "contributing_engines": result.contributing_engines,
        "safety": result.safety,
        "errors": result.errors,
    }


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_strategy_regression() -> Dict[str, Any]:
    """
    Validate the 8B strategy layer.
    """

    source = {
        "trace_id": "8B-TEST-TRACE",
        "decision": "MONITOR",
        "confidence": "LOW",
        "priority": "MEDIUM",
        "adaptation_state": "ADAPTATION_AVAILABLE",
        "learning_signal": "LEARNING_SIGNAL_AVAILABLE",
        "evidence": [
            {"source": "8A", "valid": True}
        ],
        "contributing_engines": [
            "reasoning",
            "predictive_intelligence",
        ],
    }

    result = integrate_adaptive_strategy(source)

    safety = result["safety"]

    checks = {
        "status_ready": (
            result["status"] == "READY"
        ),
        "layer_8b": (
            result["layer"] == "8B"
        ),
        "trace_preserved": (
            result["trace_id"]
            == source["trace_id"]
        ),
        "decision_preserved": (
            result["decision"]
            == source["decision"]
        ),
        "confidence_preserved": (
            result["confidence"]
            == source["confidence"]
        ),
        "priority_preserved": (
            result["priority"]
            == source["priority"]
        ),
        "adaptation_preserved": (
            result["adaptation_state"]
            == source["adaptation_state"]
        ),
        "learning_signal_preserved": (
            result["learning_signal"]
            == source["learning_signal"]
        ),
        "evidence_preserved": (
            bool(result["evidence"])
        ),
        "engines_preserved": (
            result["contributing_engines"]
            == source["contributing_engines"]
        ),
        "strategy_generated": (
            bool(result["strategy"])
        ),
        "recommendation_generated": (
            bool(result["recommendation"])
        ),
        "safety_advisory": (
            safety["safety_level"]
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            safety["execution_allowed"]
            is False
        ),
        "automatic_action_blocked": (
            safety["automatic_action_allowed"]
            is False
        ),
        "self_modification_blocked": (
            safety["self_modification_allowed"]
            is False
        ),
        "decision_override_blocked": (
            safety["decision_override_allowed"]
            is False
        ),
        "global_safety_valid": (
            validate_adaptive_strategy_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8B",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "trace_id": result["trace_id"],
        "strategy": result["strategy"],
        "recommendation": result["recommendation"],
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "checks": checks,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_strategy_status() -> Dict[str, Any]:
    """
    Return the current 8B module status.
    """

    return {
        "layer": ADAPTIVE_STRATEGY_VERSION,
        "status": ADAPTIVE_STRATEGY_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_strategy_safety()
        ),
    }