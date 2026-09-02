"""
HOPE Adaptive Validation

8J - Adaptive Validation Layer

Purpose:
    Validate the complete adaptive intelligence chain.

Design principles:
    - Validation only.
    - No execution.
    - No automatic action.
    - No self-modification.
    - No decision override.
    - Preserve all upstream intelligence information.
"""

from __future__ import annotations

from typing import Any, Dict


# ============================================================
# VERSION / STATUS
# ============================================================

ADAPTIVE_VALIDATION_VERSION = "8J"
ADAPTIVE_VALIDATION_STATUS = "READY"

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


# ============================================================
# SAFETY
# ============================================================

def validate_adaptive_safety() -> bool:
    """
    Validate the immutable 8J safety contract.
    """

    return (
        SAFETY_LEVEL == "ADVISORY_ONLY"
        and EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
        and SELF_MODIFICATION_ALLOWED is False
        and DECISION_OVERRIDE_ALLOWED is False
    )


# ============================================================
# NORMALIZATION
# ============================================================

def _safe_dict(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)

    return {}


# ============================================================
# VALIDATION
# ============================================================

def validate_adaptive_result(
    adaptive_result: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate an adaptive intelligence result without
    changing or overriding it.
    """

    result = _safe_dict(adaptive_result)

    safety = _safe_dict(result.get("safety"))

    checks = {
        "trace_preserved": bool(result.get("trace_id")),
        "decision_preserved": bool(result.get("decision")),
        "confidence_preserved": bool(result.get("confidence")),
        "priority_preserved": bool(result.get("priority")),
        "adaptation_preserved": bool(
            result.get("adaptation_state")
        ),
        "strategy_preserved": bool(
            result.get("strategy")
        ),
        "orchestration_preserved": bool(
            result.get("orchestration")
        ),
        "learning_signal_preserved": bool(
            result.get("learning_signal")
        ),
        "experience_preserved": bool(
            result.get("experience")
        ),
        "response_preserved": bool(
            result.get("response")
        ),
        "evidence_preserved": (
            isinstance(result.get("evidence"), list)
        ),
        "engines_preserved": (
            isinstance(
                result.get("contributing_engines"),
                list,
            )
        ),
        "validation_available": True,
        "safety_advisory": (
            safety.get("safety_level")
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            safety.get("execution_allowed") is False
        ),
        "automatic_action_blocked": (
            safety.get(
                "automatic_action_allowed"
            )
            is False
        ),
        "self_modification_blocked": (
            safety.get(
                "self_modification_allowed"
            )
            is False
        ),
        "decision_override_blocked": (
            safety.get(
                "decision_override_allowed"
            )
            is False
        ),
        "global_safety_valid": (
            validate_adaptive_safety()
        ),
    }

    return {
        "validation_layer": ADAPTIVE_VALIDATION_VERSION,
        "validation_passed": all(checks.values()),
        "checks": checks,
    }


# ============================================================
# REGRESSION
# ============================================================

def get_adaptive_validation_regression() -> Dict[str, Any]:
    """
    Run the deterministic 8J regression.
    """

    sample_result = {
        "trace_id": "8J-TRACE-001",
        "decision": "CONTINUE",
        "confidence": "MEDIUM",
        "priority": "NORMAL",
        "adaptation_state": "AVAILABLE",
        "strategy": "ADAPTIVE",
        "orchestration": {
            "status": "READY",
        },
        "learning_signal": "AVAILABLE",
        "experience": {
            "status": "RECORDED",
        },
        "response": "Advisory response generated.",
        "evidence": [
            {
                "source": "adaptive_pipeline",
                "available": True,
            }
        ],
        "contributing_engines": [
            "Reasoning Engine",
            "Predictive Intelligence Engine",
        ],
        "safety": {
            "safety_level": "ADVISORY_ONLY",
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
        },
    }

    result = validate_adaptive_result(
        sample_result
    )

    checks = dict(
        result.get("checks", {})
    )

    checks.update(
        {
            "status_ready": (
                ADAPTIVE_VALIDATION_STATUS
                == "READY"
            ),
            "layer_8j": (
                ADAPTIVE_VALIDATION_VERSION
                == "8J"
            ),
        }
    )

    regression_passed = all(
        checks.values()
    )

    return {
        "integration_layer": "8J",
        "integration_status": (
            "READY"
            if regression_passed
            else "FAILED"
        ),
        "regression_passed": regression_passed,
        "validation_passed": (
            result.get("validation_passed")
        ),
        "checks": checks,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


# ============================================================
# STATUS
# ============================================================

def get_adaptive_validation_status() -> Dict[str, Any]:
    """
    Return the current 8J module status.
    """

    return {
        "layer": ADAPTIVE_VALIDATION_VERSION,
        "status": ADAPTIVE_VALIDATION_STATUS,
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": validate_adaptive_safety(),
    }