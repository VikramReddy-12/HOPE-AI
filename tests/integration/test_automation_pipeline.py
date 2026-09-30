import unittest

from core.automation_engine import create_automation
from core.workflow_definition import define_workflow
from core.workflow_planning import create_workflow_plan
from core.workflow_execution_control import create_execution_control
from core.execution_request import create_execution_request
from core.controlled_action_invocation import invoke_controlled_action
from core.action_result_handling import normalize_action_result
from core.result_verification import verify_action_result
from core.automation_memory_audit import (
    clear_automation_audit,
    create_automation_audit,
    get_automation_audit_records,
)


class TestAutomationPipeline(unittest.TestCase):

    def setUp(self):
        clear_automation_audit()

    def tearDown(self):
        clear_automation_audit()

    def _run_pipeline(self):
        request = "Prepare a controlled automation workflow"

        automation = create_automation(request)
        self.assertIsInstance(automation, dict)

        workflow = define_workflow(
            request,
            name="HOPE Integration Workflow",
            steps=["prepare_execution"],
        )
        self.assertTrue(workflow["workflow_valid"])

        plan = create_workflow_plan(workflow)
        self.assertTrue(plan["plan_valid"])

        control_package = create_execution_control(plan)
        self.assertTrue(control_package["control_valid"])

        control = dict(control_package["controls"][0])
        control["workflow_id"] = control_package["workflow_id"]

        execution_request = create_execution_request(control)
        self.assertTrue(execution_request["request_valid"])

        invocation = invoke_controlled_action(execution_request)
        self.assertTrue(invocation["invocation_valid"])
        self.assertEqual(invocation["invocation_status"], "BLOCKED")

        action_result = normalize_action_result(invocation)
        self.assertTrue(action_result["result_valid"])
        self.assertEqual(action_result["result_status"], "BLOCKED")

        expected_step = {
            "step_id": execution_request["step_id"],
            "tool_id": execution_request["tool_id"],
        }

        verification = verify_action_result(
            action_result,
            expected_step,
        )
        self.assertTrue(verification["verification_valid"])
        self.assertTrue(verification["verified"])

        audit = create_automation_audit(verification)
        self.assertTrue(audit["audit_valid"])
        self.assertEqual(audit["audit_status"], "RECORDED")

        return (
            automation,
            workflow,
            plan,
            control_package,
            execution_request,
            invocation,
            action_result,
            verification,
            audit,
        )

    def test_full_automation_pipeline(self):
        self._run_pipeline()

    def test_execution_remains_disabled(self):
        results = self._run_pipeline()

        for result in results[1:]:
            self.assertFalse(result.get("execution_allowed", False))

    def test_pipeline_cannot_produce_false_success(self):
        self._run_pipeline()

        records = get_automation_audit_records()
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["result_status"], "BLOCKED")
        self.assertFalse(records[0]["execution_allowed"])

    def test_9f_remains_execution_owner(self):
        (
            _automation,
            _workflow,
            _plan,
            control_package,
            execution_request,
            _invocation,
            _result,
            _verification,
            _audit,
        ) = self._run_pipeline()

        self.assertEqual(control_package["execution_owner"], "9F")
        self.assertEqual(execution_request["execution_owner"], "9F")


if __name__ == "__main__":
    unittest.main()
