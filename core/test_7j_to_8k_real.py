from core.intelligence_orchestrator import (
    orchestrate,
    OrchestrationRequest,
)
from core.adaptive_orchestrator import (
    build_adaptive_orchestrator_result,
)

from reasoning.engine import reason

from core.predictive_intelligence import (
    get_predictive_decision_summary,
    get_predictive_decision_trace_regression,
    get_system_prediction,
)


def main():
    print("=" * 70)
    print("REAL 7J -> 8A-8J -> 8K END-TO-END TEST")
    print("=" * 70)

    # ------------------------------------------------------------
    # 1. REAL INTELLIGENCE ENGINE OUTPUTS
    # ------------------------------------------------------------

    reasoning_result = reason(
        "compare Java and Python"
    )

    prediction = get_system_prediction()

    decision_summary = get_predictive_decision_summary()

    trace_regression = (
        get_predictive_decision_trace_regression()
    )

    print("\n[1] REAL ENGINE OUTPUTS")
    print("Reasoning:", bool(reasoning_result))
    print("Prediction:", bool(prediction))
    print("Decision summary:", bool(decision_summary))

    # ------------------------------------------------------------
    # 2. 7J REQUEST WITH REAL ENGINE OUTPUTS
    # ------------------------------------------------------------

    request = OrchestrationRequest(
        command="predictive risk analysis",
        intent="PREDICT",
        requested_capabilities=[
            "reasoning",
            "predictive_risk",
        ],
        context={
            "engine_outputs": {
                "reasoning": reasoning_result,
                "predictive_prediction": prediction,
                "predictive_decision_summary": (
                    decision_summary
                ),
                "predictive_trace_regression": (
                    trace_regression
                ),
            }
        },
    )

    # ------------------------------------------------------------
    # 3. REAL 7J ORCHESTRATION
    # ------------------------------------------------------------

    orchestration_result = orchestrate(request)

    print("\n[2] 7J ORCHESTRATION")
    print("Status:", orchestration_result.status)
    print("Trace:", orchestration_result.trace_id)
    print(
        "Selected engines:",
        orchestration_result.selected_engines,
    )
    print(
        "Pipeline:",
        orchestration_result.pipeline,
    )

    if orchestration_result.errors:
        print(
            "7J errors:",
            orchestration_result.errors,
        )

    # ------------------------------------------------------------
    # 4. REAL 8K ADVISORY BRIDGE
    # ------------------------------------------------------------

    adaptive_result = build_adaptive_orchestrator_result(
        orchestration_result
    )

    print("\n[3] 8K ADAPTIVE RESULT")
    print("Status:", adaptive_result.get("status"))
    print("Trace:", adaptive_result.get("trace_id"))
    print("Decision:", adaptive_result.get("decision"))
    print("Confidence:", adaptive_result.get("confidence"))
    print("Priority:", adaptive_result.get("priority"))
    print("Strategy:", adaptive_result.get("strategy"))
    print(
        "Learning:",
        adaptive_result.get("learning_signal"),
    )
    print(
        "Experience:",
        adaptive_result.get("experience_id"),
    )
    print(
        "Response:",
        adaptive_result.get("response"),
    )
    print(
        "Engines:",
        adaptive_result.get("contributing_engines"),
    )
    print(
        "7J engines:",
        adaptive_result.get("7j_selected_engines"),
    )
    print(
        "7J pipeline:",
        adaptive_result.get("7j_pipeline"),
    )
    print(
        "Layers:",
        adaptive_result.get("contributing_layers"),
    )
    print(
        "Safety:",
        adaptive_result.get("safety"),
    )
    print(
        "Validation:",
        adaptive_result.get("validation"),
    )
    print(
        "Errors:",
        adaptive_result.get("errors"),
    )

    # ------------------------------------------------------------
    # 5. AUTHORITATIVE 7J -> 8K PRESERVATION CHECKS
    # ------------------------------------------------------------

    checks = {
        "trace_preserved": (
            adaptive_result.get("trace_id")
            == orchestration_result.trace_id
        ),

        "status_ready": (
            orchestration_result.status == "READY"
            and adaptive_result.get("status") == "READY"
        ),

        "engines_preserved": (
            adaptive_result.get("7j_selected_engines")
            == list(orchestration_result.selected_engines)
        ),

        "pipeline_preserved": (
            adaptive_result.get("7j_pipeline")
            == list(orchestration_result.pipeline)
        ),

        "decision_available": bool(
            adaptive_result.get("decision")
        ),

        "confidence_available": bool(
            adaptive_result.get("confidence")
        ),

        "priority_available": bool(
            adaptive_result.get("priority")
        ),

        "safety_advisory": (
            adaptive_result.get("safety", {}).get(
                "safety_level"
            )
            == "ADVISORY_ONLY"
        ),

        "execution_blocked": (
            adaptive_result.get("safety", {}).get(
                "execution_allowed"
            )
            is False
        ),

        "automatic_action_blocked": (
            adaptive_result.get("safety", {}).get(
                "automatic_action_allowed"
            )
            is False
        ),

        "self_modification_blocked": (
            adaptive_result.get("safety", {}).get(
                "self_modification_allowed"
            )
            is False
        ),

        "decision_override_blocked": (
            adaptive_result.get("safety", {}).get(
                "decision_override_allowed"
            )
            is False
        ),
    }

    print("\n[4] FINAL CHECKS")

    for name, passed in checks.items():
        print(
            f"{name}: {'PASS' if passed else 'FAIL'}"
        )

    passed = all(checks.values())

    print("\n" + "=" * 70)
    print(
        "REAL 7J -> 8K:",
        "PASS" if passed else "FAIL",
    )
    print("=" * 70)

    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
