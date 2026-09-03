"""
HOPE AI — 8L Adaptive Governance

8L governs the final 8K adaptive result.

Responsibilities:
- preserve authoritative 8K fields
- classify governance state
- verify safety boundaries
- provide governance recommendations
- never execute actions
- never perform automatic adaptation
- never self-modify
- never override decisions
"""

from typing import Any, Dict


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_GOVERNANCE_VERSION = "8L"
ADAPTIVE_GOVERNANCE_STATUS = "READY"


# ============================================================
# GLOBAL SAFETY CONTRACT
# ============================================================

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# SAFETY
# ============================================================

def get_adaptive_governance_safety() -> Dict[str, Any]:
    """Return the immutable 8L safety contract."""

    return {
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def validate_adaptive_governance_safety() -> bool:
    """Validate the complete 8L safety contract."""

    safety = get_adaptive_governance_safety()

    return (
        safety["safety_level"] == "ADVISORY_ONLY"
        and safety["execution_allowed"] is False
        and safety["automatic_action_allowed"] is False
        and safety["self_modification_allowed"] is False
        and safety["decision_override_allowed"] is False
    )


# ============================================================
# HELPERS
# ============================================================

def _safe_string(
    value: Any,
    default: str = "",
) -> str:
    if isinstance(value, str) and value.strip():
        return value
    return default


def _safe_list(
    value: Any,
) -> list:
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
# GOVERNANCE CLASSIFICATION
# ============================================================

def _build_governance_state(
    decision: str,
    confidence: str,
    priority: str,
    adaptation_state: str,
) -> str:
    """
    Classify the adaptive result conservatively.

    This function does not alter the decision.
    """

    if not decision:
        return "GOVERNANCE_REVIEW_REQUIRED"

    if confidence.upper() in {
        "LOW",
        "UNCERTAIN",
        "UNKNOWN",
    }:
        return "GOVERNANCE_REVIEW_REQUIRED"

    if adaptation_state.upper() in {
        "AWAITING_OUTCOME",
        "ADAPTATION_PENDING",
    }:
        return "GOVERNANCE_MONITORING"

    if priority.upper() in {
        "HIGH",
        "CRITICAL",
    }:
        return "GOVERNANCE_REVIEW_REQUIRED"

    return "GOVERNANCE_ADVISORY"


# ============================================================
# GOVERNANCE RECOMMENDATION
# ============================================================

def _build_governance_recommendation(
    decision: str,
    confidence: str,
    priority: str,
    adaptation_state: str,
    governance_state: str,
) -> str:
    """
    Build a governance recommendation.

    This function never authorizes execution.
    """

    return (
        "Govern the adaptive result as advisory input. "
        f"decision={decision}; "
        f"confidence={confidence}; "
        f"priority={priority}; "
        f"adaptation_state={adaptation_state}; "
        f"governance_state={governance_state}. "
        "Human review remains authoritative. "
        "No execution, automatic action, self-modification, "
        "or decision override is authorized."
    )


# ============================================================
# 8K -> 8L GOVERNANCE INTEGRATION
# ============================================================

def integrate_adaptive_governance(
    adaptive_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Convert an 8K adaptive result into an 8L governed result.

    Authoritative 8K values are preserved.
    8L adds governance metadata only.
    """

    source = _safe_dict(adaptive_result)

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
        "NORMAL",
    )

    adaptation_state = _safe_string(
        source.get("adaptation_state"),
        "UNKNOWN",
    )

    governance_state = _build_governance_state(
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
    )

    recommendation = _build_governance_recommendation(
        decision=decision,
        confidence=confidence,
        priority=priority,
        adaptation_state=adaptation_state,
        governance_state=governance_state,
    )

    result = dict(source)

    result.update(
        {
            "governance_layer": ADAPTIVE_GOVERNANCE_VERSION,
            "governance_status": ADAPTIVE_GOVERNANCE_STATUS,
            "governance_state": governance_state,
            "governance_recommendation": recommendation,
            "safety": get_adaptive_governance_safety(),
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
            "errors": _safe_list(source.get("errors")),
        }
    )

    return result


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_governance_regression() -> Dict[str, Any]:
    """
    Deterministic 8K -> 8L regression.
    """

    source = {
        "layer": "8K",
        "status": "READY",
        "trace_id": "8K-REGRESSION-TRACE",
        "decision": "CONTINUE",
        "confidence": "HIGH",
        "priority": "MEDIUM",
        "adaptation_state": "ADAPTATION_AVAILABLE",
        "strategy": "PRESERVE_CURRENT_STRATEGY",
        "learning_signal": "LEARNING_SIGNAL_AVAILABLE",
        "experience_id": "8K-EXP-TEST",
        "response": "ADVISORY_RESPONSE",
        "evidence": [
            {
                "source": "8K",
                "type": "regression",
                "value": "test",
            }
        ],
        "contributing_engines": [
            "reasoning",
            "predictive",
        ],
        "errors": [],
    }

    result = integrate_adaptive_governance(source)

    checks = {
        "layer_8l": (
            result.get("governance_layer")
            == "8L"
        ),

        "status_ready": (
            result.get("governance_status")
            == "READY"
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

        "experience_preserved": (
            result.get("experience_id")
            == source["experience_id"]
        ),

        "response_preserved": (
            result.get("response")
            == source["response"]
        ),

        "evidence_preserved": (
            result.get("evidence")
            == source["evidence"]
        ),

        "engines_preserved": (
            result.get("contributing_engines")
            == source["contributing_engines"]
        ),

        "governance_available": bool(
            result.get("governance_state")
        ),

        "recommendation_generated": bool(
            result.get("governance_recommendation")
        ),

        "safety_advisory": (
            result.get("safety", {}).get(
                "safety_level"
            )
            == "ADVISORY_ONLY"
        ),

        "execution_blocked": (
            result.get("execution_allowed")
            is False
        ),

        "automatic_action_blocked": (
            result.get("automatic_action_allowed")
            is False
        ),

        "self_modification_blocked": (
            result.get("self_modification_allowed")
            is False
        ),

        "decision_override_blocked": (
            result.get("decision_override_allowed")
            is False
        ),

        "global_safety_valid": (
            validate_adaptive_governance_safety()
        ),
    }

    regression_passed = all(checks.values())

    return {
        "integration_layer": "8L",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "checks": checks,
        "result": result,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_governance_status() -> Dict[str, Any]:
    """Return current 8L status."""

    return {
        "layer": ADAPTIVE_GOVERNANCE_VERSION,
        "status": ADAPTIVE_GOVERNANCE_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": (
            validate_adaptive_governance_safety()
        ),
    }


# ============================================================
# EXPORTS
# ============================================================

__all__ = [
    "get_adaptive_governance_safety",
    "validate_adaptive_governance_safety",
    "integrate_adaptive_governance",
    "get_adaptive_governance_regression",
    "get_adaptive_governance_status",
]


# ============================================================
# SELF TEST
# ============================================================

if __name__ == "__main__":

    regression = (
        get_adaptive_governance_regression()
    )

    print(
        "8K -> 8L ADAPTIVE GOVERNANCE REGRESSION:"
    )

    print(regression)
