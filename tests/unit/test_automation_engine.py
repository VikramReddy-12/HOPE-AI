import unittest

from core.automation_engine import (
    LAYER,
    STATUS,
    EXECUTION_ENABLED,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    create_automation,
    get_automation_engine_regression,
)


class TestAutomationEngine(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11A")

    def test_status(self):
        self.assertEqual(STATUS, "READY")

    def test_execution_constant_disabled(self):
        self.assertFalse(EXECUTION_ENABLED)

    def test_automatic_action_disabled(self):
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_valid_request_is_accepted(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertTrue(result["automation_valid"])

    def test_request_is_preserved(self):
        request = "Create a workflow to organize my tasks."
        result = create_automation(request)
        self.assertEqual(result["request"], request)

    def test_workflow_is_created(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertIsInstance(result["workflow"], list)
        self.assertTrue(result["workflow"])

    def test_workflow_contains_four_steps(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertEqual(result["workflow_step_count"], 4)
        self.assertEqual(len(result["workflow"]), 4)

    def test_first_step_is_proposed(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertEqual(result["workflow"][0]["status"], "PROPOSED")

    def test_second_step_is_proposed(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertEqual(result["workflow"][1]["status"], "PROPOSED")

    def test_third_step_is_proposed(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertEqual(result["workflow"][2]["status"], "PROPOSED")

    def test_execution_step_is_blocked(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertEqual(result["workflow"][3]["status"], "BLOCKED")

    def test_execution_is_not_requested(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertFalse(result["execution_requested"])

    def test_execution_remains_disabled(self):
        result = create_automation("Create a workflow to organize my tasks.")
        self.assertFalse(result["execution_allowed"])

    def test_empty_request_is_rejected(self):
        result = create_automation("")
        self.assertFalse(result["automation_valid"])

    def test_whitespace_request_is_rejected(self):
        result = create_automation("   ")
        self.assertFalse(result["automation_valid"])

    def test_none_request_is_rejected(self):
        result = create_automation(None)
        self.assertFalse(result["automation_valid"])

    def test_regression_passes(self):
        regression = get_automation_engine_regression()
        self.assertTrue(all(regression.values()))


if __name__ == "__main__":
    unittest.main()
