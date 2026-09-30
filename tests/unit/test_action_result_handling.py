import unittest

from core.action_result_handling import (
    LAYER,
    RESULT_SUCCESS,
    RESULT_FAILED,
    RESULT_BLOCKED,
    RESULT_HUMAN_REVIEW,
    normalize_action_result,
    get_action_result_regression,
)


class TestActionResultHandling(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11G")

    def test_result_constants(self):
        self.assertEqual(RESULT_SUCCESS, "SUCCESS")
        self.assertEqual(RESULT_FAILED, "FAILED")
        self.assertEqual(RESULT_BLOCKED, "BLOCKED")
        self.assertEqual(RESULT_HUMAN_REVIEW, "HUMAN_REVIEW")

    def test_regression(self):
        regression = get_action_result_regression()
        self.assertTrue(all(regression.values()))

    def test_blocked_result(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "BLOCKED",
            "execution_allowed": False,
        })

        self.assertTrue(result["result_valid"])
        self.assertEqual(result["result_status"], "BLOCKED")
        self.assertFalse(result["execution_allowed"])

    def test_failed_result(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "FAILED",
            "execution_allowed": False,
        })

        self.assertTrue(result["result_valid"])
        self.assertEqual(result["result_status"], "FAILED")
        self.assertFalse(result["execution_allowed"])

    def test_human_review_result(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "HUMAN_REVIEW",
            "execution_allowed": False,
        })

        self.assertTrue(result["result_valid"])
        self.assertEqual(result["result_status"], "HUMAN_REVIEW")
        self.assertFalse(result["execution_allowed"])

    def test_success_requires_execution_permission(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "SUCCESS",
            "execution_allowed": False,
        })

        self.assertTrue(result["result_valid"])
        self.assertEqual(result["result_status"], "SUCCESS")
        self.assertFalse(result["execution_allowed"])

    def test_success_with_execution_permission(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "SUCCESS",
            "execution_allowed": True,
        })

        self.assertTrue(result["result_valid"])
        self.assertEqual(result["result_status"], "SUCCESS")
        self.assertTrue(result["execution_allowed"])

    def test_unknown_status_does_not_become_success(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "UNKNOWN",
            "execution_allowed": True,
        })

        self.assertNotEqual(result["result_status"], "SUCCESS")
        self.assertFalse(result["execution_allowed"])

    def test_invalid_result_type(self):
        result = normalize_action_result("invalid")

        self.assertFalse(result["result_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_invalid_invocation(self):
        result = normalize_action_result({
            "invocation_valid": False,
            "invocation_status": "BLOCKED",
        })

        self.assertFalse(result["result_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_workflow_information_preserved(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "BLOCKED",
            "workflow_id": "workflow_123",
            "step_id": "step_42",
            "step_name": "test_action",
            "tool_id": "test_tool",
            "execution_allowed": False,
        })

        self.assertEqual(result["workflow_id"], "workflow_123")
        self.assertEqual(result["step_id"], "step_42")
        self.assertEqual(result["step_name"], "test_action")
        self.assertEqual(result["tool_id"], "test_tool")

    def test_safety_invariants(self):
        result = normalize_action_result({
            "invocation_valid": True,
            "invocation_status": "BLOCKED",
            "execution_allowed": False,
        })

        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])


if __name__ == "__main__":
    unittest.main()
