import unittest

from core.automation_memory_audit import (
    LAYER,
    create_automation_audit,
    get_automation_audit_records,
    clear_automation_audit,
    get_automation_memory_audit_regression,
)


class TestAutomationMemoryAudit(unittest.TestCase):

    def setUp(self):
        clear_automation_audit()

    def tearDown(self):
        clear_automation_audit()

    def test_layer(self):
        self.assertEqual(LAYER, "11I")

    def test_regression(self):
        regression = get_automation_memory_audit_regression()
        self.assertTrue(all(regression.values()))

    def test_audit_record_created(self):
        result = create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "step_name": "test_step",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        self.assertTrue(result["audit_valid"])
        self.assertEqual(result["audit_status"], "RECORDED")

    def test_audit_record_stored(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        records = get_automation_audit_records()

        self.assertEqual(len(records), 1)

    def test_multiple_records(self):
        for number in range(3):
            create_automation_audit({
                "verification_valid": True,
                "verification_status": "VERIFIED",
                "verified": True,
                "workflow_id": f"workflow_{number}",
                "step_id": f"step_{number}",
                "result_status": "BLOCKED",
                "execution_allowed": False,
            })

        self.assertEqual(len(get_automation_audit_records()), 3)

    def test_workflow_preserved(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_123",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        record = get_automation_audit_records()[0]

        self.assertEqual(record["workflow_id"], "workflow_123")

    def test_step_preserved(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_42",
            "step_name": "perform_action",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        record = get_automation_audit_records()[0]

        self.assertEqual(record["step_id"], "step_42")
        self.assertEqual(record["step_name"], "perform_action")

    def test_result_preserved(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "FAILED",
            "execution_allowed": False,
        })

        record = get_automation_audit_records()[0]

        self.assertEqual(record["result_status"], "FAILED")

    def test_verification_preserved(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        record = get_automation_audit_records()[0]

        self.assertEqual(
            record["verification_status"],
            "VERIFIED",
        )

        self.assertTrue(record["verified"])

    def test_audit_id_exists(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        record = get_automation_audit_records()[0]

        self.assertTrue(record["audit_id"])

    def test_timestamp_exists(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        record = get_automation_audit_records()[0]

        self.assertTrue(record["timestamp"])

    def test_invalid_result_rejected(self):
        result = create_automation_audit({})

        self.assertFalse(result["audit_valid"])

    def test_invalid_result_type_rejected(self):
        result = create_automation_audit("invalid")

        self.assertFalse(result["audit_valid"])

    def test_execution_disabled(self):
        result = create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        self.assertFalse(result["execution_allowed"])
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(result["decision_override_allowed"])

    def test_clear_audit(self):
        create_automation_audit({
            "verification_valid": True,
            "verification_status": "VERIFIED",
            "verified": True,
            "workflow_id": "workflow_1",
            "step_id": "step_1",
            "result_status": "BLOCKED",
            "execution_allowed": False,
        })

        self.assertEqual(len(get_automation_audit_records()), 1)

        clear_automation_audit()

        self.assertEqual(len(get_automation_audit_records()), 0)


if __name__ == "__main__":
    unittest.main()
