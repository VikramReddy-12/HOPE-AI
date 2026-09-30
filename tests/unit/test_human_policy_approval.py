import unittest

from core.human_policy_approval import (
    LAYER,
    STATUS,
    AUTOMATIC_ACTION_ALLOWED,
    SELF_MODIFICATION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    EXECUTION_ALLOWED,
    approve_verified_intent,
    get_human_policy_approval_regression,
)


class TestHumanPolicyApproval(unittest.TestCase):

    def setUp(self):
        self.verification_result = {
            "verification_passed": True,
            "verified_intent": {
                "intent_type": "memory_save",
                "tool_id": "memory_store",
                "capability": "memory",
                "request": "Remember that my favorite car is BMW 7 Series.",
                "verified": True,
                "proposed_only": True,
            },
        }

    def test_layer(self):
        self.assertEqual(LAYER, "10H")

    def test_status(self):
        self.assertEqual(STATUS, "READY")

    def test_unapproved_requires_human_review(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=False,
        )
        self.assertEqual(
            result["approval_status"],
            "HUMAN_REVIEW_REQUIRED",
        )

    def test_unapproved_is_not_granted(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=False,
        )
        self.assertFalse(result["approval_granted"])

    def test_unapproved_human_flag_is_false(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=False,
        )
        self.assertFalse(result["human_approval"])

    def test_approved_status_recorded(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertEqual(
            result["approval_status"],
            "APPROVED",
        )

    def test_approval_is_granted(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertTrue(result["approval_granted"])

    def test_human_approval_recorded(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertTrue(result["human_approval"])

    def test_verified_intent_preserved(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertEqual(
            result["verified_intent"]["tool_id"],
            "memory_store",
        )

    def test_verified_intent_remains_proposed(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertTrue(
            result["verified_intent"]["proposed_only"]
        )

    def test_invalid_verification_rejected(self):
        result = approve_verified_intent({})
        self.assertFalse(result["approval_valid"])
        self.assertFalse(result["approval_granted"])

    def test_non_dictionary_verification_rejected(self):
        result = approve_verified_intent("invalid")
        self.assertFalse(result["approval_valid"])
        self.assertFalse(result["approval_granted"])

    def test_invalid_payload_rejected(self):
        result = approve_verified_intent({
            "verification_passed": True,
            "verified_intent": None,
        })
        self.assertFalse(result["approval_valid"])
        self.assertFalse(result["approval_granted"])

    def test_non_proposed_intent_rejected(self):
        result = approve_verified_intent({
            "verification_passed": True,
            "verified_intent": {
                "intent_type": "memory_save",
                "tool_id": "memory_store",
                "capability": "memory",
                "request": "Remember this.",
                "verified": True,
                "proposed_only": False,
            },
        })
        self.assertFalse(result["approval_valid"])
        self.assertFalse(result["approval_granted"])

    def test_execution_constant_disabled(self):
        self.assertFalse(EXECUTION_ALLOWED)

    def test_execution_disabled_after_approval(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertFalse(result["automatic_action_allowed"])
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertFalse(result["self_modification_allowed"])
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        result = approve_verified_intent(
            self.verification_result,
            human_approval=True,
        )
        self.assertFalse(result["decision_override_allowed"])
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_approval_requires_successful_verification(self):
        result = approve_verified_intent({
            "verification_passed": False,
            "verified_intent": self.verification_result["verified_intent"],
        }, human_approval=True)
        self.assertFalse(result["approval_granted"])
        self.assertEqual(
            result["approval_status"],
            "REJECTED",
        )

    def test_approval_requires_proposed_only_intent(self):
        result = approve_verified_intent({
            "verification_passed": True,
            "verified_intent": {
                "intent_type": "memory_save",
                "tool_id": "memory_store",
                "capability": "memory",
                "request": "Remember this.",
                "verified": True,
                "proposed_only": False,
            },
        }, human_approval=True)
        self.assertFalse(result["approval_granted"])

    def test_regression_passes(self):
        result = get_human_policy_approval_regression()
        self.assertTrue(result["regression_passed"])


if __name__ == "__main__":
    unittest.main()
