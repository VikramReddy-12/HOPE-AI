import unittest

from core.ai_verification import (
    LAYER,
    STATUS,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    verify_tool_intent,
    get_ai_verification_regression,
)


class TestAIVerification(unittest.TestCase):

    def setUp(self):
        self.memory_intent = {
            "intent_valid": True,
            "tool_intent": {
                "intent_type": "memory_save",
                "tool_id": "memory_store",
                "capability": "memory",
                "request": "Remember that my favorite car is BMW 7 Series.",
                "proposed_only": True,
            },
        }

    def test_layer(self):
        self.assertEqual(LAYER, "10G")

    def test_status(self):
        self.assertEqual(STATUS, "READY")

    def test_valid_intent_verifies(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertTrue(result["verification_valid"])
        self.assertTrue(result["verification_passed"])

    def test_verified_tool_id_preserved(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertEqual(
            result["verified_intent"]["tool_id"],
            "memory_store",
        )

    def test_verified_capability_preserved(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertEqual(
            result["verified_intent"]["capability"],
            "memory",
        )

    def test_verified_intent_type_preserved(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertEqual(
            result["verified_intent"]["intent_type"],
            "memory_save",
        )

    def test_request_preserved(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertEqual(
            result["verified_intent"]["request"],
            "Remember that my favorite car is BMW 7 Series.",
        )

    def test_verified_flag_is_true(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertTrue(result["verified_intent"]["verified"])

    def test_verified_intent_remains_proposed(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertTrue(
            result["verified_intent"]["proposed_only"]
        )

    def test_invalid_result_rejected(self):
        result = verify_tool_intent({})
        self.assertFalse(result["verification_passed"])
        self.assertIsNone(result["verified_intent"])

    def test_non_dictionary_rejected(self):
        result = verify_tool_intent("invalid")
        self.assertFalse(result["verification_passed"])

    def test_unknown_tool_rejected(self):
        result = verify_tool_intent({
            "intent_valid": True,
            "tool_intent": {
                "intent_type": "unknown",
                "tool_id": "unknown_tool",
                "capability": "unknown",
                "request": "Do something.",
                "proposed_only": True,
            },
        })
        self.assertFalse(result["verification_passed"])

    def test_non_proposed_intent_rejected(self):
        result = verify_tool_intent({
            "intent_valid": True,
            "tool_intent": {
                "intent_type": "memory_save",
                "tool_id": "memory_store",
                "capability": "memory",
                "request": "Remember this.",
                "proposed_only": False,
            },
        })
        self.assertFalse(result["verification_passed"])

    def test_empty_request_rejected(self):
        result = verify_tool_intent({
            "intent_valid": True,
            "tool_intent": {
                "intent_type": "memory_save",
                "tool_id": "memory_store",
                "capability": "memory",
                "request": "",
                "proposed_only": True,
            },
        })
        self.assertFalse(result["verification_passed"])

    def test_execution_disabled(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        result = verify_tool_intent(self.memory_intent)
        self.assertFalse(result["decision_override_allowed"])
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_no_tool_intent_verifies(self):
        result = verify_tool_intent({
            "intent_valid": True,
            "tool_intent": {
                "intent_type": "no_tool_required",
                "tool_id": None,
                "capability": None,
                "request": "Hello HOPE.",
                "proposed_only": True,
            },
        })
        self.assertTrue(result["verification_passed"])
        self.assertIsNone(result["verified_intent"]["tool_id"])

    def test_knowledge_tool_verifies(self):
        result = verify_tool_intent({
            "intent_valid": True,
            "tool_intent": {
                "intent_type": "knowledge_lookup",
                "tool_id": "knowledge_lookup",
                "capability": "knowledge",
                "request": "What is artificial intelligence?",
                "proposed_only": True,
            },
        })
        self.assertTrue(result["verification_passed"])
        self.assertEqual(
            result["verified_intent"]["tool_id"],
            "knowledge_lookup",
        )

    def test_regression_passes(self):
        result = get_ai_verification_regression()
        self.assertTrue(result["regression_passed"])


if __name__ == "__main__":
    unittest.main()
