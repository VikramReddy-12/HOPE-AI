import unittest

from core.controlled_action_invocation import (
    LAYER,
    EXECUTION_OWNER,
    invoke_controlled_action,
    get_controlled_action_invocation_regression,
)


class TestControlledActionInvocation(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11F")

    def test_execution_owner(self):
        self.assertEqual(EXECUTION_OWNER, "9F")

    def test_regression(self):
        regression = get_controlled_action_invocation_regression()
        self.assertTrue(all(regression.values()))

    def test_valid_request_invocation(self):
        request = {
            "request_valid": True,
            "request_status": "PREPARED",
            "workflow_id": "workflow_test",
            "step_id": "step_1",
            "step_name": "test_step",
            "tool_id": None,
            "execution_requested": True,
            "execution_allowed": False,
        }

        result = invoke_controlled_action(request)

        self.assertTrue(result["invocation_valid"])
        self.assertEqual(result["invocation_status"], "BLOCKED")

    def test_missing_tool_is_blocked(self):
        request = {
            "request_valid": True,
            "request_status": "PREPARED",
            "step_id": "step_1",
            "step_name": "test_step",
            "tool_id": None,
        }

        result = invoke_controlled_action(request)

        self.assertTrue(result["invocation_valid"])
        self.assertEqual(result["invocation_status"], "BLOCKED")
        self.assertFalse(result["execution_allowed"])

    def test_invalid_request_type(self):
        result = invoke_controlled_action("invalid")

        self.assertFalse(result["invocation_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_invalid_request(self):
        result = invoke_controlled_action({})

        self.assertFalse(result["invocation_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_missing_step_id(self):
        request = {
            "request_valid": True,
            "step_name": "test_step",
        }

        result = invoke_controlled_action(request)

        self.assertFalse(result["invocation_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_missing_step_name(self):
        request = {
            "request_valid": True,
            "step_id": "step_1",
        }

        result = invoke_controlled_action(request)

        self.assertFalse(result["invocation_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_workflow_id_preserved(self):
        request = {
            "request_valid": True,
            "workflow_id": "workflow_123",
            "step_id": "step_1",
            "step_name": "test_step",
        }

        result = invoke_controlled_action(request)

        self.assertEqual(result["workflow_id"], "workflow_123")

    def test_step_information_preserved(self):
        request = {
            "request_valid": True,
            "step_id": "step_42",
            "step_name": "perform_action",
        }

        result = invoke_controlled_action(request)

        self.assertEqual(result["step_id"], "step_42")
        self.assertEqual(result["step_name"], "perform_action")

    def test_execution_owner(self):
        request = {
            "request_valid": True,
            "step_id": "step_1",
            "step_name": "test_step",
        }

        result = invoke_controlled_action(request)

        self.assertEqual(result["execution_owner"], "9F")

    def test_safety_invariants(self):
        request = {
            "request_valid": True,
            "step_id": "step_1",
            "step_name": "test_step",
        }

        result = invoke_controlled_action(request)

        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

    def test_gate_not_checked_without_tool(self):
        request = {
            "request_valid": True,
            "step_id": "step_1",
            "step_name": "test_step",
            "tool_id": None,
        }

        result = invoke_controlled_action(request)

        self.assertFalse(result["gate_checked"])

    def test_non_valid_request_rejected(self):
        request = {
            "request_valid": False,
            "step_id": "step_1",
            "step_name": "test_step",
        }

        result = invoke_controlled_action(request)

        self.assertFalse(result["invocation_valid"])
        self.assertFalse(result["execution_allowed"])


if __name__ == "__main__":
    unittest.main()
