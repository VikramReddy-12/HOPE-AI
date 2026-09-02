"""
HOPE AI — 8D Adaptive Decision Integration

Purpose:
    Convert the validated 8C adaptive orchestration result into a
    structured adaptive decision recommendation.

Design principles:
    - 8D consumes existing 8C adaptive orchestration output.
    - Existing decisions are preserved.
    - Confidence and priority are preserved.
    - Adaptation and strategy are preserved.
    - Learning signals are preserved.
    - Evidence and contributing engines are preserved.
    - 8D produces recommendations only.
    - No automatic execution is permitted.
    - No automatic system-changing action is permitted.
    - No self-modification is permitted.
    - No decision override is permitted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_DECISION_VERSION = "8D"
ADAPTIVE_DECISION_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_string(
    value: Any,
    default: str = "",
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

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8D safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_decision_safety() -> bool:
    """
    Validate the global 8D safety contract.
    """

    return (
        SAFETY_LEVEL == "ADVISORY_ONLY"
        and EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
        and SELF_MODIFICATION_ALLOWED is False
        and DECISION_OVERRIDE_ALLOWED is False
    )


# ============================================================
# RESULT MODEL
# ============================================================

@dataclass
class AdaptiveDecisionResult:
    """
    Structured 8D adaptive decision result.
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
        default_factory=_build_safety
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# DECISION EXTRACTION
# ============================================================

def _extract_decision(
    adaptive_orchestration: Dict[str, Any],
) -> str:
    """
    Preserve the existing decision.
    """

    return _safe_string(
        adaptive_orchestration.get("decision"),
        "NO_DECISION",
    )


def _extract_confidence(
    adaptive_orchestration: Dict[str, Any],
) -> str:
    """
    Preserve the existing confidence.
    """

    return _safe_string(
        adaptive_orchestration.get("confidence"),
        "UNKNOWN",
    )


def _extract_priority(
    adaptive_orchestration: Dict[str, Any],
) -> str:
    """
    Preserve the existing priority.
    """

    return _safe_string(
        adaptive_orchestration.get("priority"),
        "UNKNOWN",
    )


def _extract_adaptation_state(
    adaptive_orchestration: Dict[str, Any],
) -> str:
    """
    Preserve the 8A adaptation state.
    """

    return _safe_string(
        adaptive_orchestration.get("adaptation_state"),
        "UNKNOWN",
    )


def _extract_strategy(
    adaptive_orchestration: Dict[str, Any],
) -> str:
    """
    Preserve the 8B adaptive strategy.
    """

    return _safe_string(
        adaptive_orchestration.get("strategy"),
        "NO_STRATEGY",
    )


def _extract_learning_signal(
    adaptive_orchestration: Dict[str, Any],
) -> str:
    """
    Preserve the learning signal.
    """

    return _safe_string(
        adaptive_orchestration.get("learning_signal"),
        "INSUFFICIENT_DATA",
    )


def _extract_evidence(
    adaptive_orchestration: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Preserve existing evidence without inventing new evidence.
    """

    evidence = adaptive_orchestration.get(
        "evidence",
        [],
    )

    if not isinstance(evidence, list):
        return []

    return [
        dict(item)
        for item in evidence
        if isinstance(item, dict)
    ]


def _extract_engines(
    adaptive_orchestration: Dict[str, Any],
) -> List[str]:
    """
    Preserve contributing engines.
    """

    engines = adaptive_orchestration.get(
        "contributing_engines",
        [],
    )

    return [
        _safe_string(item)
        for item in _safe_list(engines)
        if _safe_string(item)
    ]


# ============================================================
# RECOMMENDATION
# ============================================================

def _build_recommendation(
    decision: str,
    confidence: str,
    priority: str,
    adaptation_state: str,
    strategy: str,
) -> str:
    """
    Produce an advisory recommendation.

    This function does not authorize execution.
    """

    return (
        "Adaptive decision recommendation: "
        f"decision={decision}; "
        f"confidence={confidence}; "
        f"priority={priority}; "
        f"adaptation={adaptation_state}; "
        f"strategy={strategy}. "
        "Recommendation is advisory only."
    )


# ============================================================
# INTEGRATION
# ============================================================

def integrate_adaptive_decision(
    adaptive_orchestration: Any,
) -> AdaptiveDecisionResult:
    """
    Build an 8D adaptive decision from the existing 8C result.
    """

    data = _safe_dict(
        adaptive_orchestration
    )

    trace_id = _safe_string(
        data.get("trace_id"),
        "8D-TRACE-UNKNOWN",
    )

    decision = _extract_decision(data)
    confidence = _extract_confidence(data)
    priority = _extract_priority(data)

    adaptation_state = _extract_adaptation_state(
        data
    )

    strategy = _extract_strategy(
        data
    )

    learning_signal = _extract_learning_signal(
        data
    )

    evidence = _extract_evidence(
        data
    )

    contributing_engines = _extract_engines(
        data
    )

    recommendation = _build_recommendation(
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
        strategy=strategy,
    )

    return AdaptiveDecisionResult(
        trace_id=trace_id,
        status=ADAPTIVE_DECISION_STATUS,
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
        strategy=strategy,
        recommendation=recommendation,
        learning_signal=learning_signal,
        evidence=evidence,
        contributing_engines=contributing_engines,
        safety=_build_safety(),
    )


# ============================================================
# DICT OUTPUT
# ============================================================

def adaptive_decision_to_dict(
    result: AdaptiveDecisionResult,
) -> Dict[str, Any]:
    """
    Convert the 8D result into a plain dictionary.
    """

    return {
        "layer": ADAPTIVE_DECISION_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "adaptation_state": result.adaptation_state,
        "strategy": result.strategy,
        "recommendation": result.recommendation,
        "learning_signal": result.learning_signal,
        "evidence": list(result.evidence),
        "contributing_engines": list(
            result.contributing_engines
        ),
        "safety": dict(result.safety),
        "errors": list(result.errors),
    }


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_decision_regression() -> Dict[str, Any]:
    """
    Run deterministic 8D regression checks.
    """

    source = {
        "trace_id": "8D-TEST-TRACE",
        "decision": "CONTINUE",
        "confidence": "HIGH",
        "priority": "MEDIUM",
        "adaptation_state": "ADAPTATION_AVAILABLE",
        "strategy": "PRESERVE_CURRENT_STRATEGY",
        "learning_signal": "LEARNING_SIGNAL_AVAILABLE",
        "evidence": [
            {
                "source": "8C",
                "value": "validated",
            }
        ],
        "contributing_engines": [
            "Reasoning Engine",
            "Predictive Intelligence Engine",
        ],
    }

    result = integrate_adaptive_decision(
        source
    )

    checks = {
        "status_ready": (
            result.status == "READY"
        ),
        "layer_8d": (
            ADAPTIVE_DECISION_VERSION == "8D"
        ),
        "trace_preserved": (
            result.trace_id
            == source["trace_id"]
        ),
        "decision_preserved": (
            result.decision
            == source["decision"]
        ),
        "confidence_preserved": (
            result.confidence
            == source["confidence"]
        ),
        "priority_preserved": (
            result.priority
            == source["priority"]
        ),
        "adaptation_preserved": (
            result.adaptation_state
            == source["adaptation_state"]
        ),
        "strategy_preserved": (
            result.strategy
            == source["strategy"]
        ),
        "learning_signal_preserved": (
            result.learning_signal
            == source["learning_signal"]
        ),
        "evidence_preserved": (
            bool(result.evidence)
        ),
        "engines_preserved": (
            result.contributing_engines
            == source["contributing_engines"]
        ),
        "decision_recommendation_generated": (
            bool(result.recommendation)
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
            validate_adaptive_decision_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8D",
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
        "adaptation_state": result.adaptation_state,
        "strategy": result.strategy,
        "recommendation": result.recommendation,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "checks": checks,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_decision_status() -> Dict[str, Any]:
    """
    Return the current 8D module status.
    """

    return {
        "layer": ADAPTIVE_DECISION_VERSION,
        "status": ADAPTIVE_DECISION_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": validate_adaptive_decision_safety(),
    }