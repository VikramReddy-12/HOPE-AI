"""
HOPE Adaptive Learning Intelligence

v1.6 - 8F Adaptive Learning

Purpose:
    Convert validated adaptive-response and learning-feedback
    information into a structured learning recommendation.

Design principles:
    - 8F analyzes; it does not self-modify HOPE.
    - Existing decisions are preserved.
    - Existing learning signals are preserved.
    - Traceability is preserved.
    - Evidence and contributing engines are preserved.
    - Learning recommendations remain advisory.
    - No automatic execution is permitted.
    - No automatic action is permitted.
    - No self-modification is permitted.
    - No decision override is permitted.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_LEARNING_VERSION = "8F"
ADAPTIVE_LEARNING_STATUS = "READY"

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
    """
    Convert a value into a safe string.
    """

    if value is None:
        return default

    value = str(value).strip()

    return value if value else default


def _safe_list(
    value: Any,
) -> List[Any]:
    """
    Return a defensive list copy.
    """

    if value is None:
        return []

    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    return [value]


def _safe_dict(
    value: Any,
) -> Dict[str, Any]:
    """
    Return a defensive dictionary copy.
    """

    if isinstance(value, dict):
        return dict(value)

    return {}


# ============================================================
# SAFETY
# ============================================================

def _build_safety() -> Dict[str, Any]:
    """
    Return the immutable 8F safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_learning_safety() -> bool:
    """
    Validate the 8F safety boundary.
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
class AdaptiveLearningResult:
    """
    Structured 8F adaptive-learning result.
    """

    trace_id: str

    status: str

    decision: str
    confidence: str
    priority: str

    learning_signal: str

    adaptation_state: Dict[str, Any]

    strategy: Dict[str, Any]

    response_recommendation: str

    evidence: List[Dict[str, Any]]

    contributing_engines: List[str]

    learning_recommendation: str

    safety: Dict[str, Any] = field(
        default_factory=_build_safety
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# LEARNING RECOMMENDATION
# ============================================================

def _build_learning_recommendation(
    decision: str,
    confidence: str,
    priority: str,
    learning_signal: str,
    adaptation_state: Dict[str, Any],
    strategy: Dict[str, Any],
) -> str:
    """
    Build a transparent learning recommendation.

    This function produces guidance only.
    It does not change models, memory, decisions, or code.
    """

    decision = _safe_string(
        decision,
        "UNKNOWN",
    )

    confidence = _safe_string(
        confidence,
        "UNKNOWN",
    )

    priority = _safe_string(
        priority,
        "UNKNOWN",
    )

    learning_signal = _safe_string(
        learning_signal,
        "UNKNOWN",
    )

    adaptation_state = _safe_dict(
        adaptation_state
    )

    strategy = _safe_dict(
        strategy
    )

    adaptation = _safe_string(
        adaptation_state.get("state")
        or adaptation_state.get("adaptation_state"),
        "UNKNOWN",
    )

    strategy_name = _safe_string(
        strategy.get("strategy")
        or strategy.get("recommended_strategy")
        or strategy.get("recommendation"),
        "UNKNOWN",
    )

    if learning_signal == "LEARNING_SIGNAL_AVAILABLE":
        learning_action = (
            "Retain the observed learning signal for future "
            "advisory evaluation."
        )
    elif learning_signal in {
        "INSUFFICIENT_DATA",
        "INSUFFICIENT_FEEDBACK",
        "MISSING_FEEDBACK",
    }:
        learning_action = (
            "Collect additional outcome evidence before "
            "drawing a stronger learning conclusion."
        )
    else:
        learning_action = (
            "Treat the current learning signal as advisory "
            "until sufficient evidence is available."
        )

    return (
        f"Decision: {decision}. "
        f"Confidence: {confidence}. "
        f"Priority: {priority}. "
        f"Adaptive state: {adaptation}. "
        f"Strategy: {strategy_name}. "
        f"Learning signal: {learning_signal}. "
        f"{learning_action} "
        "No automatic learning or self-modification is authorized."
    )


# ============================================================
# INTEGRATION
# ============================================================

def integrate_adaptive_learning(
    adaptive_response: Any,
) -> Dict[str, Any]:
    """
    Integrate the existing 8E adaptive response into 8F.

    Upstream information is preserved rather than replaced.
    """

    source = _safe_dict(
        adaptive_response
    )

    trace_id = _safe_string(
        source.get("trace_id"),
        "8F-UNKNOWN",
    )

    decision = _safe_string(
        source.get("decision"),
        "UNKNOWN",
    )

    confidence = _safe_string(
        source.get("confidence"),
        "UNKNOWN",
    )

    priority = _safe_string(
        source.get("priority"),
        "UNKNOWN",
    )

    learning_signal = _safe_string(
        source.get("learning_signal"),
        "UNKNOWN",
    )

    adaptation_state = _safe_dict(
        source.get("adaptation_state")
    )

    strategy = _safe_dict(
        source.get("strategy")
    )

    response_recommendation = _safe_string(
        source.get("response_recommendation")
    )

    evidence = _safe_list(
        source.get("evidence")
    )

    contributing_engines = _safe_list(
        source.get("contributing_engines")
    )

    learning_recommendation = (
        _build_learning_recommendation(
            decision=decision,
            confidence=confidence,
            priority=priority,
            learning_signal=learning_signal,
            adaptation_state=adaptation_state,
            strategy=strategy,
        )
    )

    result = AdaptiveLearningResult(
        trace_id=trace_id,
        status=ADAPTIVE_LEARNING_STATUS,
        decision=decision,
        confidence=confidence,
        priority=priority,
        learning_signal=learning_signal,
        adaptation_state=adaptation_state,
        strategy=strategy,
        response_recommendation=response_recommendation,
        evidence=[
            item
            for item in evidence
            if isinstance(item, dict)
        ],
        contributing_engines=[
            _safe_string(item)
            for item in contributing_engines
            if _safe_string(item)
        ],
        learning_recommendation=(
            learning_recommendation
        ),
        safety=_build_safety(),
    )

    return {
        "layer": ADAPTIVE_LEARNING_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "learning_signal": result.learning_signal,
        "adaptation_state": result.adaptation_state,
        "strategy": result.strategy,
        "response_recommendation": (
            result.response_recommendation
        ),
        "learning_recommendation": (
            result.learning_recommendation
        ),
        "evidence": result.evidence,
        "contributing_engines": (
            result.contributing_engines
        ),
        "safety": result.safety,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "errors": result.errors,
    }


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_learning_regression() -> Dict[str, Any]:
    """
    Run the complete 8F regression.
    """

    source = {
        "trace_id": "8F-REGRESSION-TRACE",
        "decision": "CONTINUE",
        "confidence": "HIGH",
        "priority": "MEDIUM",
        "learning_signal": (
            "LEARNING_SIGNAL_AVAILABLE"
        ),
        "adaptation_state": {
            "state": "ADAPTED",
            "source": "8A",
        },
        "strategy": {
            "strategy": "ADAPTIVE_CONTINUATION",
            "recommendation": (
                "Continue with the validated strategy."
            ),
        },
        "response_recommendation": (
            "Advisory response preserved."
        ),
        "evidence": [
            {
                "source": "reasoning",
                "value": "validated",
            },
            {
                "source": "predictive",
                "value": "validated",
            },
        ],
        "contributing_engines": [
            "Reasoning Engine",
            "Predictive Intelligence Engine",
            "Adaptive Intelligence",
            "Adaptive Strategy",
            "Adaptive Orchestration",
            "Adaptive Decision",
            "Adaptive Response",
        ],
    }

    result = integrate_adaptive_learning(
        source
    )

    checks = {
        "status_ready": (
            result.get("status")
            == "READY"
        ),

        "layer_8f": (
            result.get("layer")
            == "8F"
        ),

        "trace_preserved": (
            result.get("trace_id")
            == source["trace_id"]
        ),

        "decision_preserved": (
            result.get("decision")
            == source["decision"]
        ),

        "confidence_preserved": (
            result.get("confidence")
            == source["confidence"]
        ),

        "priority_preserved": (
            result.get("priority")
            == source["priority"]
        ),

        "learning_signal_preserved": (
            result.get("learning_signal")
            == source["learning_signal"]
        ),

        "adaptation_preserved": (
            result.get("adaptation_state")
            == source["adaptation_state"]
        ),

        "strategy_preserved": (
            result.get("strategy")
            == source["strategy"]
        ),

        "response_preserved": (
            result.get("response_recommendation")
            == source["response_recommendation"]
        ),

        "evidence_preserved": (
            len(result.get("evidence", []))
            == len(source["evidence"])
        ),

        "engines_preserved": (
            result.get("contributing_engines")
            == source["contributing_engines"]
        ),

        "learning_recommendation_generated": (
            bool(
                result.get(
                    "learning_recommendation"
                )
            )
        ),

        "safety_advisory": (
            result["safety"]["safety_level"]
            == "ADVISORY_ONLY"
        ),

        "execution_blocked": (
            result["safety"]["execution_allowed"]
            is False
        ),

        "automatic_action_blocked": (
            result["safety"][
                "automatic_action_allowed"
            ]
            is False
        ),

        "self_modification_blocked": (
            result["safety"][
                "self_modification_allowed"
            ]
            is False
        ),

        "decision_override_blocked": (
            result["safety"][
                "decision_override_allowed"
            ]
            is False
        ),

        "global_safety_valid": (
            validate_adaptive_learning_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8F",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "trace_id": result.get("trace_id"),
        "learning_recommendation": (
            result.get(
                "learning_recommendation"
            )
        ),
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "checks": checks,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_learning_status() -> Dict[str, Any]:
    """
    Return the current 8F module status.
    """

    return {
        "layer": ADAPTIVE_LEARNING_VERSION,
        "status": ADAPTIVE_LEARNING_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_learning_safety()
        ),
    }