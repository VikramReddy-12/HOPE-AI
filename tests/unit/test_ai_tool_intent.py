import unittest

from core.ai_tool_intent import (
    LAYER,
    STATUS,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    create_tool_intent,
    get_ai_tool_intent_regression,
)


class TestAIToolIntent(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "10F")

    def test_status(self):
        self.assertEqual(STATUS, "READY")

    def test_memory_intent_is_valid(self):
        result = create_tool_intent(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertTrue(result["intent_valid"])

    def test_memory_tool_selected(self):
        result = create_tool_intent(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertEqual(
            result["tool_intent"]["tool_id"],
            "memory_store",
        )

    def test_memory_capability_selected(self):
        result = create_tool_intent(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertEqual(
            result["tool_intent"]["capability"],
            "memory",
        )

    def test_memory_intent_type(self):
        result = create_tool_intent(
            "Remember that my favorite car is BMW 7 Series."
        )
        self.assertEqual(
            result["tool_intent"]["intent_type"],
            "memory_save",
        )

    def test_knowledge_intent_is_valid(self):
        result = create_tool_intent(
            "What is artificial intelligence?"
        )
        self.assertTrue(result["intent_valid"])

    def test_knowledge_tool_selected(self):
        result = create_tool_intent(
            "What is artificial intelligence?"
        )
        self.assertEqual(
            result["tool_intent"]["tool_id"],
            "knowledge_lookup",
        )

    def test_knowledge_capability_selected(self):
        result = create_tool_intent(
            "What is artificial intelligence?"
        )
        self.assertEqual(
            result["tool_intent"]["capability"],
            "knowledge",
        )

    def test_knowledge_intent_type(self):
        result = create_tool_intent(
            "What is artificial intelligence?"
        )
        self.assertEqual(
            result["tool_intent"]["intent_type"],
            "knowledge_lookup",
        )

    def test_neutral_request_requires_no_tool(self):
        result = create_tool_intent("Hello HOPE.")
        self.assertTrue(result["intent_valid"])
        self.assertEqual(
            result["tool_intent"]["intent_type"],
            "no_tool_required",
        )
        self.assertIsNone(result["tool_intent"]["tool_id"])

    def test_tool_intent_is_proposed_only(self):
        result = create_tool_intent("Remember this.")
        self.assertTrue(
            result["tool_intent"]["proposed_only"]
        )

    def test_execution_not_requested(self):
        result = create_tool_intent("Remember this.")
        self.assertFalse(result["execution_requested"])

    def test_execution_disabled(self):
        result = create_tool_intent("Remember this.")
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = create_tool_intent("Remember this.")
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        result = create_tool_intent("Remember this.")
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        result = create_tool_intent("Remember this.")
        self.assertFalse(result["decision_override_allowed"])
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_empty_request_rejected(self):
        result = create_tool_intent("")
        self.assertFalse(result["intent_valid"])
        self.assertIsNone(result["tool_intent"])

    def test_none_request_rejected(self):
        result = create_tool_intent(None)
        self.assertFalse(result["intent_valid"])

    def test_invalid_plan_rejected(self):
        result = create_tool_intent(
            "Remember this.",
            plan=[],
        )
        self.assertFalse(result["intent_valid"])
        self.assertIsNone(result["tool_intent"])

    def test_valid_plan_accepted(self):
        result = create_tool_intent(
            "Remember this.",
            plan={
                "plan_valid": True,
                "plan": [],
            },
        )
        self.assertTrue(result["intent_valid"])

    def test_request_is_preserved(self):
        request = "  Remember that HOPE is my AI project.  "
        result = create_tool_intent(request)
        self.assertEqual(
            result["request"],
            "Remember that HOPE is my AI project.",
        )

    def test_regression_passes(self):
        result = get_ai_tool_intent_regression()
        self.assertTrue(result["regression_passed"])


if __name__ == "__main__":
    unittest.main()
