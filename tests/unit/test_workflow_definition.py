import unittest

from core.workflow_definition import (
    LAYER,
    STATUS,
    EXECUTION_ENABLED,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    define_workflow,
    get_workflow_definition_regression,
)


class TestWorkflowDefinition(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11B")

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

    def test_valid_workflow_is_accepted(self):
        result = define_workflow(
            "Organize my daily tasks.",
            "Daily Task Workflow",
            ["collect_tasks", "prioritize_tasks"],
        )
        self.assertTrue(result["workflow_valid"])

    def test_workflow_id_is_present(self):
        result = define_workflow("Organize my tasks.")
        self.assertTrue(result["workflow_id"])

    def test_workflow_name_is_preserved(self):
        result = define_workflow(
            "Organize my tasks.",
            "My Task Workflow",
        )
        self.assertEqual(result["name"], "My Task Workflow")

    def test_request_is_preserved(self):
        request = "Organize my daily tasks."
        result = define_workflow(request)
        self.assertEqual(result["request"], request)

    def test_default_workflow_contains_one_step(self):
        result = define_workflow("Organize my tasks.")
        self.assertEqual(result["step_count"], 1)
        self.assertEqual(len(result["steps"]), 1)

    def test_custom_workflow_step_count(self):
        result = define_workflow(
            "Organize my tasks.",
            steps=["collect", "prioritize", "summarize"],
        )
        self.assertEqual(result["step_count"], 3)

    def test_steps_are_proposed(self):
        result = define_workflow(
            "Organize my tasks.",
            steps=["collect", "prioritize", "summarize"],
        )
        self.assertTrue(
            all(step["status"] == "PROPOSED" for step in result["steps"])
        )

    def test_step_ids_are_created(self):
        result = define_workflow(
            "Organize my tasks.",
            steps=["collect", "prioritize"],
        )
        self.assertEqual(result["steps"][0]["step_id"], "step_1")
        self.assertEqual(result["steps"][1]["step_id"], "step_2")

    def test_dependencies_are_created(self):
        result = define_workflow(
            "Organize my tasks.",
            steps=["collect", "prioritize", "summarize"],
        )
        self.assertEqual(result["dependencies"][0]["depends_on"], [])
        self.assertEqual(
            result["dependencies"][1]["depends_on"],
            ["step_1"],
        )
        self.assertEqual(
            result["dependencies"][2]["depends_on"],
            ["step_2"],
        )

    def test_workflow_status_is_proposed(self):
        result = define_workflow("Organize my tasks.")
        self.assertEqual(result["workflow_status"], "PROPOSED")

    def test_execution_is_not_requested(self):
        result = define_workflow("Organize my tasks.")
        self.assertFalse(result["execution_requested"])

    def test_execution_remains_disabled(self):
        result = define_workflow("Organize my tasks.")
        self.assertFalse(result["execution_allowed"])

    def test_empty_request_is_rejected(self):
        result = define_workflow("")
        self.assertFalse(result["workflow_valid"])

    def test_whitespace_request_is_rejected(self):
        result = define_workflow("   ")
        self.assertFalse(result["workflow_valid"])

    def test_none_request_is_rejected(self):
        result = define_workflow(None)
        self.assertFalse(result["workflow_valid"])

    def test_invalid_steps_are_rejected(self):
        result = define_workflow(
            "Organize my tasks.",
            steps="invalid",
        )
        self.assertFalse(result["workflow_valid"])

    def test_regression_passes(self):
        regression = get_workflow_definition_regression()
        self.assertTrue(all(regression.values()))


if __name__ == "__main__":
    unittest.main()
