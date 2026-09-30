import unittest

from core.runtime_ownership import (
    get_runtime_ownership,
    get_action_migration_candidates,
    get_legacy_runtime_responsibilities,
    get_runtime_ownership_status,
    get_runtime_ownership_regression,
)


class TestRuntimeOwnership(unittest.TestCase):

    def test_brain_owns_request_understanding(self):
        ownership = get_runtime_ownership()
        self.assertEqual(
            ownership["request_understanding"],
            "brain",
        )

    def test_r1_owns_runtime_integration(self):
        ownership = get_runtime_ownership()
        self.assertEqual(
            ownership["runtime_integration"],
            "r1",
        )

    def test_orchestration_owner(self):
        ownership = get_runtime_ownership()
        self.assertEqual(
            ownership["orchestration"],
            "7J_8A_8N",
        )

    def test_controlled_execution_owner(self):
        ownership = get_runtime_ownership()
        self.assertEqual(
            ownership["controlled_execution"],
            "9F",
        )

    def test_legacy_router_remains_transitional_owner(self):
        ownership = get_runtime_ownership()
        self.assertEqual(
            ownership["legacy_execution"],
            "router",
        )

    def test_action_migration_candidates(self):
        candidates = get_action_migration_candidates()

        expected = [
            "MEMORY_SAVE",
            "MEMORY_RECALL",
            "KNOWLEDGE_SEARCH",
            "COMPARE",
            "RECOMMEND",
            "GOAL",
            "STUDY_PLAN",
        ]

        for intent in expected:
            self.assertEqual(
                candidates[intent],
                "9A_9I",
            )

    def test_legacy_runtime_responsibilities(self):
        responsibilities = get_legacy_runtime_responsibilities()

        self.assertEqual(
            responsibilities["GREETING"],
            "router",
        )
        self.assertEqual(
            responsibilities["HELP"],
            "router",
        )
        self.assertEqual(
            responsibilities["RECOVERY"],
            "router",
        )
        self.assertEqual(
            responsibilities["EXIT"],
            "router",
        )

    def test_execution_remains_disabled(self):
        status = get_runtime_ownership_status()

        self.assertFalse(status["execution_enabled"])
        self.assertFalse(status["automatic_action_allowed"])
        self.assertFalse(status["self_modification_allowed"])
        self.assertFalse(status["decision_override_allowed"])

    def test_regression_passes(self):
        result = get_runtime_ownership_regression()

        self.assertTrue(
            result["regression_passed"]
        )


if __name__ == "__main__":
    unittest.main()
