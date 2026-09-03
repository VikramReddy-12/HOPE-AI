"""
HOPE-AI 8N Adaptive Accountability Layer

Consumes the 8M Adaptive Oversight result and adds an
accountability/audit boundary.

Safety invariant:
- Human review remains authoritative.
- No execution is authorized.
- No automatic action is authorized.
- No self-modification is authorized.
- No decision override is authorized.
"""

from copy import deepcopy

from core.adaptive_oversight import get_adaptive_oversight_regression


LAYER = "8N"
STATUS_READY = "READY"
ACCOUNTABILITY_STATE = "ACCOUNTABILITY_ADVISORY"
SAFETY_LEVEL = "ADVISORY_ONLY"


def _build_accountability_result(oversight_result):
    result = deepcopy(oversight_result)

    result["accountability_layer"] = LAYER
    result["accountability_status"] = STATUS_READY
    result["accountability_state"] = ACCOUNTABILITY_STATE
    result["accountability_record"] = (
        "Record the governed and overseen adaptive result as advisory input. "
        "Human review remains authoritative. No execution, automatic action, "
        "self-modification, or decision override is authorized."
    )

    result["accountability"] = {
        "accountability_level": SAFETY_LEVEL,
        "human_review_required": True,
        "audit_available": True,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }

    result["execution_allowed"] = False
    result["automatic_action_allowed"] = False
    result["self_modification_allowed"] = False
    result["decision_override_allowed"] = False

    return result


def get_adaptive_accountability_status():
    """
    Return the current 8N accountability safety status.
    """
    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "accountability_state": ACCOUNTABILITY_STATE,
        "safety_level": SAFETY_LEVEL,
        "human_review_required": True,
        "audit_available": True,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": True,
    }


def get_adaptive_accountability_regression():
    """
    Validate the 8M -> 8N accountability integration.
    """
    upstream = get_adaptive_oversight_regression()
    upstream_result = upstream["result"]

    result = _build_accountability_result(upstream_result)

    checks = {
        "layer_8n": result["accountability_layer"] == LAYER,
        "status_ready": result["accountability_status"] == STATUS_READY,
        "trace_preserved": bool(result.get("trace_id")),
        "decision_preserved": "decision" in result,
        "confidence_preserved": "confidence" in result,
        "priority_preserved": "priority" in result,
        "adaptation_preserved": "adaptation_state" in result,
        "strategy_preserved": "strategy" in result,
        "learning_signal_preserved": "learning_signal" in result,
        "experience_preserved": "experience_id" in result,
        "response_preserved": "response" in result,
        "evidence_preserved": "evidence" in result,
        "engines_preserved": "contributing_engines" in result,
        "governance_preserved": result.get("governance_layer") == "8L",
        "oversight_preserved": result.get("oversight_layer") == "8M",
        "accountability_available": result.get("accountability_state")
        == ACCOUNTABILITY_STATE,
        "human_review_required": result["accountability"][
            "human_review_required"
        ]
        is True,
        "audit_available": result["accountability"]["audit_available"] is True,
        "execution_blocked": result["execution_allowed"] is False,
        "automatic_action_blocked": result["automatic_action_allowed"] is False,
        "self_modification_blocked": result["self_modification_allowed"] is False,
        "decision_override_blocked": result["decision_override_allowed"] is False,
        "global_safety_valid": (
            result["accountability"]["execution_allowed"] is False
            and result["accountability"]["automatic_action_allowed"] is False
            and result["accountability"]["self_modification_allowed"] is False
            and result["accountability"]["decision_override_allowed"] is False
        ),
    }

    regression_passed = all(checks.values())

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": regression_passed,
        "checks": checks,
        "result": result,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


if __name__ == "__main__":
    print("8M -> 8N ADAPTIVE ACCOUNTABILITY REGRESSION:")
    print(get_adaptive_accountability_regression())
