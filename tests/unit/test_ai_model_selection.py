import unittest

from core.ai_model_selection import (
    AUTOMATIC_ACTION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    LAYER,
    SELF_MODIFICATION_ALLOWED,
    STATUS,
    _request_requirements,
    get_model_selection_regression,
    select_model,
)


class TestAIModelSelection(unittest.TestCase):

    def test_selection_layer(self):
        self.assertEqual(LAYER, "10C")

    def test_selection_status(self):
        self.assertEqual(STATUS, "READY")

    def test_reasoning_requirement_detection(self):
        requirements = _request_requirements(
            "Analyze and compare this architecture."
        )

        self.assertTrue(
            requirements["reasoning_required"]
        )

    def test_coding_requirement_detection(self):
        requirements = _request_requirements(
            "Write Python code to debug this program."
        )

        self.assertTrue(
            requirements["coding_required"]
        )

    def test_general_assistance_is_available(self):
        requirements = _request_requirements(
            "Tell me about this project."
        )

        self.assertTrue(
            requirements["general_assistance"]
        )

    def test_tool_requirement_detection(self):
        requirements = _request_requirements(
            "Execute this action using a tool."
        )

        self.assertTrue(
            requirements["tool_use_required"]
        )

    def test_reasoning_model_selection(self):
        result = select_model(
            "Analyze and compare the HOPE architecture."
        )

        self.assertTrue(
            result["selection_available"]
        )

        self.assertIsNotNone(
            result["selected_model"]
        )

        self.assertEqual(
            result["selected_model"]["provider"],
            "openai",
        )

        self.assertEqual(
            result["selected_model"]["model_id"],
            "gpt-5.6-luna",
        )

    def test_selection_candidates_present(self):
        result = select_model(
            "Analyze the HOPE architecture."
        )

        self.assertGreaterEqual(
            len(result["candidates"]),
            1,
        )

    def test_selected_model_has_score(self):
        result = select_model(
            "Analyze the HOPE architecture."
        )

        selected = result["selected_model"]

        self.assertIn(
            "score",
            selected,
        )

        self.assertGreaterEqual(
            selected["score"],
            0,
        )

    def test_selection_does_not_execute_actions(self):
        result = select_model(
            "Execute an action using a tool."
        )

        self.assertFalse(
            result["automatic_action_allowed"]
        )

    def test_self_modification_disabled(self):
        self.assertFalse(
            SELF_MODIFICATION_ALLOWED
        )

    def test_decision_override_disabled(self):
        self.assertFalse(
            DECISION_OVERRIDE_ALLOWED
        )

    def test_selection_regression_passes(self):
        result = get_model_selection_regression()

        self.assertTrue(
            result["regression_passed"]
        )


if __name__ == "__main__":
    unittest.main()
