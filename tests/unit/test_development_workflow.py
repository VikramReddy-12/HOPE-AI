import unittest

from core.development_workflow import (
    create_development_workflow,
    get_development_workflow_regression,
)


class TestDevelopmentWorkflow(unittest.TestCase):

    def test_regression_passes(self):
        result = get_development_workflow_regression()

        self.assertTrue(result["regression_passed"])
        self.assertFalse(result["execution_enabled"])

    def test_project_inspect_selected(self):
        result = create_development_workflow(
            "Inspect the project."
        )

        self.assertTrue(result["workflow_valid"])
        self.assertEqual(
            result["selected_tool"]["tool_id"],
            "project_inspect",
        )

    def test_execution_remains_disabled(self):
        result = create_development_workflow(
            "Inspect the project."
        )

        self.assertFalse(result["execution_enabled"])
        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

    def test_execution_owner_is_9f(self):
        result = create_development_workflow(
            "Inspect the project."
        )

        self.assertEqual(
            result["control_package"]["execution_owner"],
            "9F",
        )


if __name__ == "__main__":
    unittest.main()
