"""
HOPE AI - 8M Adaptive Oversight / Assurance

8M provides advisory oversight over the governed 8L adaptive result.

Safety boundary:
- Advisory only
- No execution
- No automatic action
- No self-modification
- No decision override
- Human review remains authoritative
"""


def _build_assurance_recommendation(result):
    decision = result.get("decision")
    confidence = result.get("confidence")
    priority = result.get("priority")
    governance_state = result.get("governance_state")

    return (
        "Assure the governed adaptive result as advisory input. "
        f"decision={decision}; "
        f"confidence={confidence}; "
        f"priority={priority}; "
        f"governance_state={governance_state}. "
        "Human review remains authoritative. "
        "No execution, automatic action, self-modification, "
        "or decision override is authorized."
    )


def build_adaptive_oversight_result(governed_result):
    """
    Build the 8M oversight result from an 8L governed result.
    """

    if not isinstance(governed_result, dict):
        raise TypeError("governed_result must be a dictionary")

    safety = governed_result.get("safety", {})

    result = dict(governed_result)

    result.update(
        {
            "oversight_layer": "8M",
            "oversight_status": "READY",
            "oversight_state": "ASSURANCE_ADVISORY",
            "oversight_recommendation": (
                _build_assurance_recommendation(governed_result)
            ),
            "safety": {
                "safety_level": "ADVISORY_ONLY",
                "execution_allowed": False,
                "automatic_action_allowed": False,
                "self_modification_allowed": False,
                "decision_override_allowed": False,
            },
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
        }
    )

    # Preserve the original 8L safety boundary if it was valid.
    if safety.get("safety_level") == "ADVISORY_ONLY":
        result["safety"]["safety_level"] = "ADVISORY_ONLY"

    return result


def get_adaptive_oversight_regression():
    """
    Regression test for the 8L -> 8M assurance boundary.
    """

    governed_result = {
        "layer": "8K",
        "status": "READY",
        "trace_id": "8L-REGRESSION-TRACE",
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
        "governance_layer": "8L",
        "governance_status": "READY",
        "governance_state": "GOVERNANCE_ADVISORY",
        "safety": {
            "safety_level": "ADVISORY_ONLY",
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
        },
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }

    result = build_adaptive_oversight_result(
        governed_result
    )

    checks = {
        "layer_8m": (
            result.get("oversight_layer") == "8M"
        ),
        "status_ready": (
            result.get("oversight_status") == "READY"
        ),
        "trace_preserved": (
            result.get("trace_id")
            == governed_result.get("trace_id")
        ),
        "decision_preserved": (
            result.get("decision")
            == governed_result.get("decision")
        ),
        "confidence_preserved": (
            result.get("confidence")
            == governed_result.get("confidence")
        ),
        "priority_preserved": (
            result.get("priority")
            == governed_result.get("priority")
        ),
        "adaptation_preserved": (
            result.get("adaptation_state")
            == governed_result.get("adaptation_state")
        ),
        "strategy_preserved": (
            result.get("strategy")
            == governed_result.get("strategy")
        ),
        "learning_signal_preserved": (
            result.get("learning_signal")
            == governed_result.get("learning_signal")
        ),
        "experience_preserved": (
            result.get("experience_id")
            == governed_result.get("experience_id")
        ),
        "response_preserved": (
            result.get("response")
            == governed_result.get("response")
        ),
        "evidence_preserved": (
            result.get("evidence")
            == governed_result.get("evidence")
        ),
        "engines_preserved": (
            result.get("contributing_engines")
            == governed_result.get("contributing_engines")
        ),
        "governance_preserved": (
            result.get("governance_layer") == "8L"
            and result.get("governance_status") == "READY"
            and result.get("governance_state")
            == "GOVERNANCE_ADVISORY"
        ),
        "recommendation_generated": bool(
            result.get("oversight_recommendation")
        ),
        "assurance_available": (
            result.get("oversight_state")
            == "ASSURANCE_ADVISORY"
        ),
        "safety_advisory": (
            result.get("safety", {}).get(
                "safety_level"
            )
            == "ADVISORY_ONLY"
        ),
        "execution_blocked": (
            result.get("execution_allowed") is False
        ),
        "automatic_action_blocked": (
            result.get("automatic_action_allowed") is False
        ),
        "self_modification_blocked": (
            result.get("self_modification_allowed") is False
        ),
        "decision_override_blocked": (
            result.get("decision_override_allowed") is False
        ),
    }

    return {
        "integration_layer": "8M",
        "integration_status": "READY",
        "regression_passed": all(checks.values()),
        "checks": checks,
        "result": result,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def get_adaptive_oversight_status():
    """
    Return the authoritative 8M safety/status boundary.
    """

    return {
        "layer": "8M",
        "status": "READY",
        "oversight_state": "ASSURANCE_ADVISORY",
        "safety_level": "ADVISORY_ONLY",
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "safety_valid": True,
    }


if __name__ == "__main__":
    print("8L -> 8M ADAPTIVE OVERSIGHT REGRESSION:")
    print(get_adaptive_oversight_regression())
