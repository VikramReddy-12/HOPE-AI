import unittest

from core.result_verification import (
    LAYER,
    verify_action_result,
    get_result_verification_regression,
)


class TestResultVerification(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11H")

    def test_regression(self):
        regression = get_result_verification_regression()
        self.assertTrue(all(regression.values()))

    def test_blocked_result_verified(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "BLOCKED",
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "step_name": "test_step",
            "tool_id": None,
            "execution_allowed": False,
        })

        self.assertTrue(result["verification_valid"])
        self.assertTrue(result["verified"])
        self.assertEqual(result["verification_status"], "VERIFIED")

    def test_failed_result_verified(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "FAILED",
            "step_id": "step_1",
            "execution_allowed": False,
        })

        self.assertTrue(result["verification_valid"])
        self.assertTrue(result["verified"])

    def test_human_review_verified(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "HUMAN_REVIEW",
            "step_id": "step_1",
            "execution_allowed": False,
        })

        self.assertTrue(result["verification_valid"])
        self.assertTrue(result["verified"])

    def test_false_success_rejected(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "SUCCESS",
            "step_id": "step_1",
            "execution_allowed": False,
        })

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_success_with_execution_allowed(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "SUCCESS",
            "step_id": "step_1",
            "execution_allowed": True,
        })

        self.assertTrue(result["verification_valid"])
        self.assertTrue(result["verified"])
        self.assertTrue(result["execution_allowed"])

    def test_step_mismatch_rejected(self):
        result = verify_action_result(
            {
                "result_valid": True,
                "result_status": "BLOCKED",
                "step_id": "step_2",
                "tool_id": None,
                "execution_allowed": False,
            },
            {
                "step_id": "step_1",
                "tool_id": None,
            },
        )

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_tool_mismatch_rejected(self):
        result = verify_action_result(
            {
                "result_valid": True,
                "result_status": "BLOCKED",
                "step_id": "step_1",
                "tool_id": "tool_b",
                "execution_allowed": False,
            },
            {
                "step_id": "step_1",
                "tool_id": "tool_a",
            },
        )

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_invalid_result_type(self):
        result = verify_action_result("invalid")

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_invalid_result(self):
        result = verify_action_result({})

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_unknown_status_rejected(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "UNKNOWN",
            "execution_allowed": False,
        })

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_invalid_expected_step(self):
        result = verify_action_result(
            {
                "result_valid": True,
                "result_status": "BLOCKED",
                "step_id": "step_1",
                "execution_allowed": False,
            },
            "invalid",
        )

        self.assertFalse(result["verification_valid"])
        self.assertFalse(result["verified"])

    def test_safety_invariants(self):
        result = verify_action_result({
            "result_valid": True,
            "result_status": "BLOCKED",
            "step_id": "step_1",
            "execution_allowed": False,
        })

        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])


if __name__ == "__main__":
    unittest.main()
