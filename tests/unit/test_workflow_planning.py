import unittest

from core.workflow_planning import (
    LAYER,
    STATUS,
    EXECUTION_ENABLED,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    create_workflow_plan,
    get_workflow_planning_regression,
)
from core.workflow_definition import define_workflow


class TestWorkflowPlanning(unittest.TestCase):

    def _workflow(self):
        return define_workflow(
            "Organize my daily tasks.",
            "Daily Task Workflow",
            [
                "collect_tasks",
                "prioritize_tasks",
                "prepare_summary",
            ],
        )

    def test_layer(self):
        self.assertEqual(LAYER, "11C")

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

    def test_valid_workflow_creates_plan(self):
        result = create_workflow_plan(self._workflow())
        self.assertTrue(result["plan_valid"])

    def test_workflow_id_is_preserved(self):
        workflow = self._workflow()
        result = create_workflow_plan(workflow)
        self.assertEqual(result["workflow_id"], workflow["workflow_id"])

    def test_plan_contains_three_steps(self):
        result = create_workflow_plan(self._workflow())
        self.assertEqual(result["plan_step_count"], 3)
        self.assertEqual(len(result["plan"]), 3)

    def test_plan_steps_are_planned(self):
        result = create_workflow_plan(self._workflow())
        self.assertTrue(
            all(step["status"] == "PLANNED" for step in result["plan"])
        )

    def test_step_ids_are_preserved(self):
        result = create_workflow_plan(self._workflow())
        self.assertEqual(result["plan"][0]["step_id"], "step_1")
        self.assertEqual(result["plan"][1]["step_id"], "step_2")
        self.assertEqual(result["plan"][2]["step_id"], "step_3")

    def test_step_names_are_preserved(self):
        result = create_workflow_plan(self._workflow())
        self.assertEqual(result["plan"][0]["name"], "collect_tasks")
        self.assertEqual(result["plan"][1]["name"], "prioritize_tasks")
        self.assertEqual(result["plan"][2]["name"], "prepare_summary")

    def test_dependencies_are_preserved(self):
        result = create_workflow_plan(self._workflow())
        self.assertEqual(result["plan"][0]["depends_on"], [])
        self.assertEqual(result["plan"][1]["depends_on"], ["step_1"])
        self.assertEqual(result["plan"][2]["depends_on"], ["step_2"])

    def test_plan_status_is_ready_for_control(self):
        result = create_workflow_plan(self._workflow())
        self.assertEqual(result["plan_status"], "READY_FOR_CONTROL")

    def test_execution_is_not_requested(self):
        result = create_workflow_plan(self._workflow())
        self.assertFalse(result["execution_requested"])

    def test_execution_remains_disabled(self):
        result = create_workflow_plan(self._workflow())
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_remains_disabled(self):
        result = create_workflow_plan(self._workflow())
        self.assertFalse(result["automatic_action_allowed"])

    def test_self_modification_remains_disabled(self):
        result = create_workflow_plan(self._workflow())
        self.assertFalse(result["self_modification_allowed"])

    def test_decision_override_remains_disabled(self):
        result = create_workflow_plan(self._workflow())
        self.assertFalse(result["decision_override_allowed"])

    def test_invalid_workflow_definition_is_rejected(self):
        result = create_workflow_plan({})
        self.assertFalse(result["plan_valid"])

    def test_none_definition_is_rejected(self):
        result = create_workflow_plan(None)
        self.assertFalse(result["plan_valid"])

    def test_non_dictionary_definition_is_rejected(self):
        result = create_workflow_plan("invalid")
        self.assertFalse(result["plan_valid"])

    def test_invalid_workflow_flag_is_rejected(self):
        result = create_workflow_plan(
            {
                "workflow_valid": False,
                "steps": [{"step_id": "step_1", "name": "test"}],
            }
        )
        self.assertFalse(result["plan_valid"])

    def test_missing_steps_are_rejected(self):
        result = create_workflow_plan(
            {
                "workflow_valid": True,
                "workflow_id": "test",
            }
        )
        self.assertFalse(result["plan_valid"])

    def test_empty_steps_are_rejected(self):
        result = create_workflow_plan(
            {
                "workflow_valid": True,
                "workflow_id": "test",
                "steps": [],
            }
        )
        self.assertFalse(result["plan_valid"])

    def test_regression_passes(self):
        regression = get_workflow_planning_regression()
        self.assertTrue(all(regression.values()))


if __name__ == "__main__":
    unittest.main()
