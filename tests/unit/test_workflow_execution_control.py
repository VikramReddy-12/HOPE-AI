import unittest

from core.workflow_execution_control import (
    LAYER,
    EXECUTION_OWNER,
    create_execution_control,
    evaluate_step_execution,
    get_workflow_execution_control_regression,
)


class TestWorkflowExecutionControl(unittest.TestCase):

    def test_layer(self):
        self.assertEqual(LAYER, "11D")

    def test_execution_owner(self):
        self.assertEqual(EXECUTION_OWNER, "9F")

    def test_regression(self):
        regression = get_workflow_execution_control_regression()
        self.assertTrue(all(regression.values()))

    def test_valid_plan(self):
        plan = {
            "plan_valid": True,
            "workflow_id": "test_workflow",
            "plan": [
                {
                    "plan_step": 1,
                    "step_id": "step_1",
                    "name": "test_step",
                    "depends_on": [],
                    "status": "PLANNED",
                }
            ],
        }

        result = create_execution_control(plan)

        self.assertTrue(result["control_valid"])
        self.assertEqual(result["workflow_id"], "test_workflow")
        self.assertEqual(result["control_step_count"], 1)

    def test_step_without_tool_is_blocked(self):
        step = {
            "step_id": "step_1",
            "name": "test_step",
        }

        result = evaluate_step_execution(step)

        self.assertTrue(result["control_valid"])
        self.assertEqual(result["control_status"], "BLOCKED")
        self.assertFalse(result["execution_allowed"])

    def test_invalid_step_type(self):
        result = evaluate_step_execution("invalid")

        self.assertFalse(result["control_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_missing_step_id(self):
        result = evaluate_step_execution({
            "name": "test_step",
        })

        self.assertFalse(result["control_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_missing_step_name(self):
        result = evaluate_step_execution({
            "step_id": "step_1",
        })

        self.assertFalse(result["control_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_invalid_workflow_plan_type(self):
        result = create_execution_control("invalid")

        self.assertFalse(result["control_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_invalid_workflow_plan(self):
        result = create_execution_control({})

        self.assertFalse(result["control_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_empty_plan(self):
        result = create_execution_control({
            "plan_valid": True,
            "workflow_id": "test",
            "plan": [],
        })

        self.assertFalse(result["control_valid"])
        self.assertFalse(result["execution_allowed"])

    def test_all_steps_remain_blocked(self):
        plan = {
            "plan_valid": True,
            "workflow_id": "test_workflow",
            "plan": [
                {
                    "step_id": "step_1",
                    "name": "first_step",
                },
                {
                    "step_id": "step_2",
                    "name": "second_step",
                },
            ],
        }

        result = create_execution_control(plan)

        self.assertTrue(
            all(
                control["execution_allowed"] is False
                for control in result["controls"]
            )
        )

    def test_execution_owner_is_9f(self):
        plan = {
            "plan_valid": True,
            "workflow_id": "test_workflow",
            "plan": [
                {
                    "step_id": "step_1",
                    "name": "test_step",
                }
            ],
        }

        result = create_execution_control(plan)

        self.assertEqual(result["execution_owner"], "9F")

    def test_execution_disabled(self):
        plan = {
            "plan_valid": True,
            "workflow_id": "test_workflow",
            "plan": [
                {
                    "step_id": "step_1",
                    "name": "test_step",
                }
            ],
        }

        result = create_execution_control(plan)

        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])


if __name__ == "__main__":
    unittest.main()
