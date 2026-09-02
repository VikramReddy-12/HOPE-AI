"""
HOPE Adaptive Response Intelligence

v1.6 - 8E Adaptive Response

Purpose:
    Convert the validated adaptive decision and strategy state
    into a structured response recommendation.

Design principles:
    - 8E consumes existing intelligence; it does not invent it.
    - Traceability is preserved.
    - Decision, confidence, priority, strategy, and adaptation
      state are preserved.
    - Responses remain advisory.
    - No execution is permitted.
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

ADAPTIVE_RESPONSE_VERSION = "8E"
ADAPTIVE_RESPONSE_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# TRACE
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

    if isinstance(value, list):
        return list(value)

    if isinstance(value, tuple):
        return list(value)

    if value is None:
        return []

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
    Return the immutable 8E safety contract.
    """

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_response_safety() -> bool:
    """
    Validate the 8E safety boundary.
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
class AdaptiveResponseResult:
    """
    Structured 8E adaptive-response result.
    """

    trace_id: str

    status: str

    decision: str
    confidence: str
    priority: str

    adaptation_state: Dict[str, Any]

    strategy: Dict[str, Any]

    learning_signal: str

    evidence: List[Dict[str, Any]]

    contributing_engines: List[str]

    response_recommendation: str

    safety: Dict[str, Any] = field(
        default_factory=_build_safety
    )

    errors: List[str] = field(
        default_factory=list
    )


# ============================================================
# RESPONSE RECOMMENDATION
# ============================================================

def _build_response_recommendation(
    decision: str,
    confidence: str,
    priority: str,
    strategy: Dict[str, Any],
    adaptation_state: Dict[str, Any],
    learning_signal: str,
) -> str:
    """
    Build a transparent response recommendation.

    This function does not execute the recommendation.
    """

    decision = _safe_string(
        decision,
        "No decision available.",
    )

    confidence = _safe_string(
        confidence,
        "UNKNOWN",
    )

    priority = _safe_string(
        priority,
        "UNKNOWN",
    )

    strategy = _safe_dict(strategy)
    adaptation_state = _safe_dict(adaptation_state)

    strategy_recommendation = _safe_string(
        strategy.get("recommendation")
        or strategy.get("strategy")
        or strategy.get("recommended_strategy"),
        "No adaptive strategy recommendation available.",
    )

    adaptation = _safe_string(
        adaptation_state.get("state")
        or adaptation_state.get("adaptation_state"),
        "UNKNOWN",
    )

    learning = _safe_string(
        learning_signal,
        "UNKNOWN",
    )

    return (
        f"Decision: {decision}. "
        f"Confidence: {confidence}. "
        f"Priority: {priority}. "
        f"Adaptive state: {adaptation}. "
        f"Strategy: {strategy_recommendation} "
        f"Learning signal: {learning}. "
        "Response remains advisory and requires human review."
    )


# ============================================================
# INTEGRATION
# ============================================================

def integrate_adaptive_response(
    adaptive_decision: Any,
) -> Dict[str, Any]:
    """
    Integrate the existing 8D adaptive decision into 8E.

    The input is preserved rather than replaced.
    """

    source = _safe_dict(adaptive_decision)

    trace_id = _safe_string(
        source.get("trace_id"),
        "8E-UNKNOWN",
    )

    decision = _safe_string(
        source.get("decision"),
        source.get("recommended_decision", "UNKNOWN"),
    )

    confidence = _safe_string(
        source.get("confidence"),
        "UNKNOWN",
    )

    priority = _safe_string(
        source.get("priority"),
        "UNKNOWN",
    )

    adaptation_state = _safe_dict(
        source.get("adaptation_state")
    )

    strategy = _safe_dict(
        source.get("strategy")
        or source.get("adaptive_strategy")
    )

    learning_signal = _safe_string(
        source.get("learning_signal"),
        "UNKNOWN",
    )

    evidence = _safe_list(
        source.get("evidence")
    )

    contributing_engines = _safe_list(
        source.get("contributing_engines")
        or source.get("engines")
    )

    response_recommendation = (
        _build_response_recommendation(
            decision=decision,
            confidence=confidence,
            priority=priority,
            strategy=strategy,
            adaptation_state=adaptation_state,
            learning_signal=learning_signal,
        )
    )

    result = AdaptiveResponseResult(
        trace_id=trace_id,
        status=ADAPTIVE_RESPONSE_STATUS,
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
        strategy=strategy,
        learning_signal=learning_signal,
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
        response_recommendation=response_recommendation,
        safety=_build_safety(),
    )

    return {
        "layer": ADAPTIVE_RESPONSE_VERSION,
        "status": result.status,
        "trace_id": result.trace_id,
        "decision": result.decision,
        "confidence": result.confidence,
        "priority": result.priority,
        "adaptation_state": result.adaptation_state,
        "strategy": result.strategy,
        "learning_signal": result.learning_signal,
        "evidence": result.evidence,
        "contributing_engines": result.contributing_engines,
        "response_recommendation": (
            result.response_recommendation
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

def get_adaptive_response_regression() -> Dict[str, Any]:
    """
    Run the complete 8E regression.

    The regression validates preservation of upstream
    adaptive intelligence and the 8E safety contract.
    """

    source = {
        "trace_id": "8E-REGRESSION-TRACE",
        "decision": "CONTINUE",
        "confidence": "HIGH",
        "priority": "MEDIUM",
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
        "learning_signal": (
            "LEARNING_SIGNAL_AVAILABLE"
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
        ],
    }

    result = integrate_adaptive_response(
        source
    )

    checks = {
        "status_ready": (
            result.get("status")
            == "READY"
        ),

        "layer_8e": (
            result.get("layer")
            == "8E"
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

        "adaptation_preserved": (
            result.get("adaptation_state")
            == source["adaptation_state"]
        ),

        "strategy_preserved": (
            result.get("strategy")
            == source["strategy"]
        ),

        "learning_signal_preserved": (
            result.get("learning_signal")
            == source["learning_signal"]
        ),

        "evidence_preserved": (
            len(result.get("evidence", []))
            == len(source["evidence"])
        ),

        "engines_preserved": (
            result.get("contributing_engines")
            == source["contributing_engines"]
        ),

        "response_generated": (
            bool(
                result.get(
                    "response_recommendation"
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
            validate_adaptive_response_safety()
        ),
    }

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8E",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "trace_id": result.get("trace_id"),
        "response_recommendation": (
            result.get(
                "response_recommendation"
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

def get_adaptive_response_status() -> Dict[str, Any]:
    """
    Return the current 8E module status.
    """

    return {
        "layer": ADAPTIVE_RESPONSE_VERSION,
        "status": ADAPTIVE_RESPONSE_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_response_safety()
        ),
    }