import unittest

from core.ai_decision_integration import (
    LAYER,
    STATUS,
    EXECUTION_ALLOWED,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    integrate_ai_decision,
    get_ai_decision_integration_regression,
)


class TestAIDecisionIntegration(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "10I")

    def test_status(self):
        self.assertEqual(STATUS, "READY")

    def test_memory_decision_is_valid(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertTrue(result["decision_valid"])

    def test_memory_requires_human_review(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertEqual(
            result["decision_status"],
            "HUMAN_REVIEW_REQUIRED",
        )

    def test_memory_model_selection_is_present(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertIsNotNone(result["model_selection"])

    def test_memory_plan_is_present(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertIsNotNone(result["plan"])

    def test_memory_tool_intent_is_present(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertEqual(
            result["tool_intent"]["tool_intent"]["tool_id"],
            "memory_store",
        )

    def test_memory_verification_passes(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertTrue(
            result["verification"]["verification_passed"]
        )

    def test_memory_approval_requires_human(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertEqual(
            result["approval"]["approval_status"],
            "HUMAN_REVIEW_REQUIRED",
        )

    def test_knowledge_decision_is_valid(self):
        result = integrate_ai_decision(
            "What is artificial intelligence?"
        )
        self.assertTrue(result["decision_valid"])

    def test_knowledge_tool_is_selected(self):
        result = integrate_ai_decision(
            "What is artificial intelligence?"
        )
        self.assertEqual(
            result["tool_intent"]["tool_intent"]["tool_id"],
            "knowledge_lookup",
        )

    def test_knowledge_verification_passes(self):
        result = integrate_ai_decision(
            "What is artificial intelligence?"
        )
        self.assertTrue(
            result["verification"]["verification_passed"]
        )

    def test_knowledge_requires_human_review(self):
        result = integrate_ai_decision(
            "What is artificial intelligence?"
        )
        self.assertEqual(
            result["decision_status"],
            "HUMAN_REVIEW_REQUIRED",
        )

    def test_neutral_request_is_valid(self):
        result = integrate_ai_decision("Hello")
        self.assertTrue(result["decision_valid"])

    def test_neutral_request_requires_no_approval(self):
        result = integrate_ai_decision("Hello")
        self.assertEqual(
            result["decision_status"],
            "NOT_REQUIRED",
        )

    def test_neutral_request_requires_no_model_selection(self):
        result = integrate_ai_decision("Hello")
        self.assertIsNone(result["model_selection"])

    def test_neutral_request_requires_no_plan(self):
        result = integrate_ai_decision("Hello")
        self.assertIsNone(result["plan"])

    def test_neutral_request_requires_no_tool(self):
        result = integrate_ai_decision("Hello")
        self.assertIsNone(
            result["tool_intent"]["tool_intent"]["tool_id"]
        )

    def test_neutral_request_is_verified(self):
        result = integrate_ai_decision("Hello")
        self.assertTrue(
            result["verification"]["verification_passed"]
        )

    def test_invalid_request_is_rejected(self):
        result = integrate_ai_decision("")
        self.assertFalse(result["decision_valid"])
        self.assertEqual(
            result["decision_status"],
            "REJECTED",
        )

    def test_execution_constant_disabled(self):
        self.assertFalse(EXECUTION_ALLOWED)

    def test_execution_remains_disabled(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertFalse(result["decision_override_allowed"])
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_approval_cannot_enable_execution(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertTrue(
            result["approval"]["approval_valid"]
        )
        self.assertFalse(
            result["approval"]["execution_allowed"]
        )
        self.assertFalse(result["execution_allowed"])

    def test_request_is_preserved(self):
        request = "Remember that my favorite car is BMW 7 Series."
        result = integrate_ai_decision(request)
        self.assertEqual(result["request"], request)

    def test_context_contains_selected_model_for_tool_request(self):
        result = integrate_ai_decision(
            "What is artificial intelligence?"
        )
        self.assertIsNotNone(
            result["context_package"]["context"]["selected_model"]
        )

    def test_pipeline_contains_all_controlled_stages(self):
        result = integrate_ai_decision(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertIn("model_selection", result)
        self.assertIn("context_package", result)
        self.assertIn("plan", result)
        self.assertIn("tool_intent", result)
        self.assertIn("verification", result)
        self.assertIn("approval", result)

    def test_regression_passes(self):
        result = get_ai_decision_integration_regression()
        self.assertTrue(result["regression_passed"])


if __name__ == "__main__":
    unittest.main()
