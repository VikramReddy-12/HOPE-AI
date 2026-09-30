import unittest

from core.ai_planning import (
    LAYER,
    STATUS,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    create_plan,
    get_ai_planning_regression,
)


class TestAIPlanning(unittest.TestCase):

    def setUp(self):
        self.context_package = {
            "layer": "10D",
            "status": "READY",
            "request_valid": True,
            "context": {
                "user_request": "Analyze the HOPE architecture.",
                "conversation": "Previous discussion.",
                "memory": {"project": "HOPE-AI"},
                "knowledge": {"topic": "AI architecture"},
                "reasoning": {"analysis": "Layered architecture"},
                "goals": {"goal": "Build HOPE AI"},
                "adaptive_intelligence": {
                    "strategy": "Incremental SDLC"
                },
                "selected_model": {
                    "provider": "openai",
                    "model_id": "gpt-5.6-luna",
                },
            },
        }

    def test_layer(self):
        self.assertEqual(LAYER, "10E")

    def test_status(self):
        self.assertEqual(STATUS, "READY")

    def test_plan_is_created(self):
        result = create_plan(self.context_package)
        self.assertTrue(result["plan_valid"])

    def test_plan_is_list(self):
        result = create_plan(self.context_package)
        self.assertIsInstance(result["plan"], list)

    def test_plan_contains_four_steps(self):
        result = create_plan(self.context_package)
        self.assertEqual(result["plan_step_count"], 4)

    def test_request_preserved(self):
        result = create_plan(self.context_package)
        self.assertEqual(
            result["request"],
            "Analyze the HOPE architecture.",
        )

    def test_first_step_understands_request(self):
        result = create_plan(self.context_package)
        self.assertEqual(
            result["plan"][0]["action"],
            "understand_request",
        )

    def test_second_step_evaluates_context(self):
        result = create_plan(self.context_package)
        self.assertEqual(
            result["plan"][1]["action"],
            "evaluate_context",
        )

    def test_third_step_determines_next_step(self):
        result = create_plan(self.context_package)
        self.assertEqual(
            result["plan"][2]["action"],
            "determine_next_step",
        )

    def test_fourth_step_prepares_policy(self):
        result = create_plan(self.context_package)
        self.assertEqual(
            result["plan"][3]["action"],
            "prepare_for_policy",
        )

    def test_execution_not_requested(self):
        result = create_plan(self.context_package)
        self.assertFalse(result["execution_requested"])

    def test_execution_disabled(self):
        result = create_plan(self.context_package)
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = create_plan(self.context_package)
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        result = create_plan(self.context_package)
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        result = create_plan(self.context_package)
        self.assertFalse(result["decision_override_allowed"])
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_invalid_context_rejected(self):
        result = create_plan({})
        self.assertFalse(result["plan_valid"])

    def test_non_dictionary_context_rejected(self):
        result = create_plan("invalid")
        self.assertFalse(result["plan_valid"])

    def test_empty_request_rejected(self):
        context = {
            "context": {
                "user_request": ""
            }
        }
        result = create_plan(context)
        self.assertFalse(result["plan_valid"])

    def test_regression_passes(self):
        result = get_ai_planning_regression()
        self.assertTrue(result["regression_passed"])


if __name__ == "__main__":
    unittest.main()
