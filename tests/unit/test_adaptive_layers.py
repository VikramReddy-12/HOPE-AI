import unittest

from core.adaptive_intelligence import get_adaptive_intelligence_regression
from core.adaptive_strategy import get_adaptive_strategy_regression
from core.adaptive_orchestration import get_adaptive_orchestration_regression
from core.adaptive_decision import get_adaptive_decision_regression
from core.adaptive_response import get_adaptive_response_regression
from core.adaptive_learning import get_adaptive_learning_regression
from core.adaptive_experience import get_adaptive_experience_regression
from core.adaptive_integration import get_adaptive_integration_regression
from core.adaptive_validation import get_adaptive_validation_regression
from core.adaptive_orchestrator import get_adaptive_orchestration_regression
from core.adaptive_governance import get_adaptive_governance_regression
from core.adaptive_oversight import get_adaptive_oversight_regression
from core.adaptive_accountability import get_adaptive_accountability_regression


class TestAdaptiveLayers(unittest.TestCase):

    def test_8a(self):
        result = get_adaptive_intelligence_regression()
        self.assertTrue(result["regression_passed"])

    def test_8b(self):
        result = get_adaptive_strategy_regression()
        self.assertTrue(result["regression_passed"])

    def test_8c(self):
        result = get_adaptive_orchestration_regression()
        self.assertTrue(result["regression_passed"])

    def test_8d(self):
        result = get_adaptive_decision_regression()
        self.assertTrue(result["regression_passed"])

    def test_8e(self):
        result = get_adaptive_response_regression()
        self.assertTrue(result["regression_passed"])

    def test_8f(self):
        result = get_adaptive_learning_regression()
        self.assertTrue(result["regression_passed"])

    def test_8g(self):
        result = get_adaptive_experience_regression()
        self.assertTrue(result["regression_passed"])

    def test_8h(self):
        result = get_adaptive_integration_regression()
        self.assertTrue(result["regression_passed"])

    def test_8j(self):
        result = get_adaptive_validation_regression()
        self.assertTrue(result["regression_passed"])

    def test_8k(self):
        result = get_adaptive_orchestration_regression()
        self.assertTrue(result["regression_passed"])

    def test_8l(self):
        result = get_adaptive_governance_regression()
        self.assertTrue(result["regression_passed"])

    def test_8m(self):
        result = get_adaptive_oversight_regression()
        self.assertTrue(result["regression_passed"])

    def test_8n(self):
        result = get_adaptive_accountability_regression()
        self.assertTrue(result["regression_passed"])

        self.assertEqual(result["integration_layer"], "8N")
        self.assertEqual(result["integration_status"], "READY")

        output = result["result"]

        self.assertEqual(
            output["accountability_layer"],
            "8N",
        )
        self.assertEqual(
            output["accountability_status"],
            "READY",
        )
        self.assertEqual(
            output["accountability_state"],
            "ACCOUNTABILITY_ADVISORY",
        )

        self.assertEqual(
            output["accountability"]["accountability_level"],
            "ADVISORY_ONLY",
        )
        self.assertTrue(
            output["accountability"]["human_review_required"]
        )
        self.assertTrue(
            output["accountability"]["audit_available"]
        )

        self.assertFalse(output["execution_allowed"])
        self.assertFalse(output["automatic_action_allowed"])
        self.assertFalse(output["self_modification_allowed"])
        self.assertFalse(output["decision_override_allowed"])

        self.assertFalse(
            output["accountability"]["execution_allowed"]
        )
        self.assertFalse(
            output["accountability"]["automatic_action_allowed"]
        )
        self.assertFalse(
            output["accountability"]["self_modification_allowed"]
        )
        self.assertFalse(
            output["accountability"]["decision_override_allowed"]
        )


if __name__ == "__main__":
    unittest.main()





