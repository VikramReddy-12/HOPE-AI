import unittest

from core.execution_request import (
    LAYER,
    EXECUTION_OWNER,
    create_execution_request,
    get_execution_request_regression,
)


class TestExecutionRequest(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11E")

    def test_execution_owner(self):
        self.assertEqual(EXECUTION_OWNER, "9F")

    def test_regression(self):
        regression = get_execution_request_regression()
        self.assertTrue(all(regression.values()))

    def test_valid_control_prepared(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "workflow_id": "workflow_test",
            "step_id": "step_1",
            "name": "test_step",
            "tool_id": None,
            "execution_allowed": False,
        }

        result = create_execution_request(control)

        self.assertTrue(result["request_valid"])
        self.assertEqual(result["request_status"], "PREPARED")

    def test_execution_requested(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "workflow_id": "workflow_test",
            "step_id": "step_1",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertTrue(result["execution_requested"])

    def test_execution_remains_disabled(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "step_id": "step_1",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

    def test_invalid_control_type(self):
        result = create_execution_request("invalid")

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_invalid_control(self):
        result = create_execution_request({})

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_non_blocked_control_rejected(self):
        control = {
            "control_valid": True,
            "control_status": "READY",
            "step_id": "step_1",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_missing_step_id(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_missing_step_name(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "step_id": "step_1",
        }

        result = create_execution_request(control)

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_workflow_id_preserved(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "workflow_id": "workflow_123",
            "step_id": "step_1",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertEqual(result["workflow_id"], "workflow_123")

    def test_step_information_preserved(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "step_id": "step_42",
            "name": "perform_action",
        }

        result = create_execution_request(control)

        self.assertEqual(result["step_id"], "step_42")
        self.assertEqual(result["step_name"], "perform_action")

    def test_execution_owner_preserved(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "step_id": "step_1",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertEqual(result["execution_owner"], "9F")

    def test_no_tool_is_allowed(self):
        control = {
            "control_valid": True,
            "control_status": "BLOCKED",
            "step_id": "step_1",
            "name": "test_step",
        }

        result = create_execution_request(control)

        self.assertIsNone(result["tool_id"])
        self.assertFalse(result["gate_checked"])
        self.assertFalse(result["execution_allowed"])


if __name__ == "__main__":
    unittest.main()
