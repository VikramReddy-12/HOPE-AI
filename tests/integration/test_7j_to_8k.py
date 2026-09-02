import unittest

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


class Test7JTo8KIntegration(unittest.TestCase):

    def test_real_7j_to_8k(self):
        reasoning_result = reason("compare Java and Python")
        prediction = get_system_prediction()
        decision_summary = get_predictive_decision_summary()
        trace_regression = get_predictive_decision_trace_regression()

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
                    "predictive_decision_summary": decision_summary,
                    "predictive_trace_regression": trace_regression,
                }
            },
        )

        result_7j = orchestrate(request)

        self.assertEqual(result_7j.status, "READY")
        self.assertTrue(result_7j.trace_id)
        self.assertTrue(result_7j.selected_engines)
        self.assertTrue(result_7j.pipeline)
        self.assertFalse(result_7j.errors)

        result_8k = build_adaptive_orchestrator_result(result_7j)

        self.assertEqual(result_8k.get("status"), "READY")
        self.assertEqual(
            result_8k.get("trace_id"),
            result_7j.trace_id,
        )

        self.assertEqual(
            result_8k.get("7j_selected_engines"),
            list(result_7j.selected_engines),
        )

        self.assertEqual(
            result_8k.get("7j_pipeline"),
            list(result_7j.pipeline),
        )

        self.assertTrue(result_8k.get("decision"))
        self.assertTrue(result_8k.get("confidence"))
        self.assertTrue(result_8k.get("priority"))
        self.assertTrue(result_8k.get("strategy"))
        self.assertTrue(result_8k.get("learning_signal"))
        self.assertTrue(result_8k.get("experience_id"))
        self.assertTrue(result_8k.get("response"))

        safety = result_8k.get("safety", {})

        self.assertEqual(
            safety.get("safety_level"),
            "ADVISORY_ONLY",
        )
        self.assertFalse(safety.get("execution_allowed"))
        self.assertFalse(safety.get("automatic_action_allowed"))
        self.assertFalse(safety.get("self_modification_allowed"))
        self.assertFalse(safety.get("decision_override_allowed"))

        validation = result_8k.get("validation", {})

        self.assertEqual(
            validation.get("validation_layer"),
            "8J",
        )
        self.assertTrue(
            validation.get("validation_passed")
        )

        self.assertEqual(
            result_8k.get("errors"),
            [],
        )


if __name__ == "__main__":
    unittest.main()
