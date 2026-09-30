import unittest

from core.runtime_adapter import (
    RUNTIME_OWNERSHIP,
    adapt_runtime,
    get_runtime_ownership,
    get_runtime_ownership_status,
)


class TestRuntimeOwnership(unittest.TestCase):

    def test_brain_owns_request_understanding(self):
        self.assertEqual(
            RUNTIME_OWNERSHIP["brain"],
            "request_understanding",
        )

    def test_r1_owns_runtime_integration(self):
        self.assertEqual(
            RUNTIME_OWNERSHIP["r1"],
            "runtime_integration",
        )

    def test_orchestration_owner(self):
        self.assertEqual(
            RUNTIME_OWNERSHIP["orchestration"],
            "7J_8A_8N",
        )

    def test_capability_architecture_owner(self):
        self.assertEqual(
            RUNTIME_OWNERSHIP[
                "capability_action_architecture"
            ],
            "9A_9I",
        )

    def test_controlled_execution_owner(self):
        self.assertEqual(
            RUNTIME_OWNERSHIP["controlled_execution"],
            "9F",
        )

    def test_legacy_router_remains_execution_owner(self):
        self.assertEqual(
            RUNTIME_OWNERSHIP["legacy_execution"],
            "router",
        )

    def test_runtime_exposes_ownership(self):
        result = adapt_runtime(
            {
                "intent": "MEMORY_RECALL",
                "command": "recall test_r1",
            }
        )

        ownership = result["runtime"]["ownership"]

        self.assertEqual(
            ownership["r1"],
            "runtime_integration",
        )

        self.assertEqual(
            ownership["legacy_execution"],
            "router",
        )

    def test_ownership_function_returns_copy(self):
        ownership = get_runtime_ownership()

        self.assertEqual(
            ownership,
            RUNTIME_OWNERSHIP,
        )

        self.assertIsNot(
            ownership,
            RUNTIME_OWNERSHIP,
        )

    def test_safety_remains_disabled(self):
        status = get_runtime_ownership_status()

        self.assertFalse(
            status["execution_enabled"]
        )

        self.assertFalse(
            status["automatic_action_allowed"]
        )

        self.assertFalse(
            status["self_modification_allowed"]
        )

        self.assertFalse(
            status["decision_override_allowed"]
        )

    def test_legacy_execution_is_explicitly_transitional(self):
        status = get_runtime_ownership_status()

        self.assertEqual(
            status["controlled_execution_owner"],
            "9F",
        )

        self.assertEqual(
            status["legacy_execution_owner"],
            "router",
        )

        self.assertTrue(
            status["legacy_execution_active"]
        )


if __name__ == "__main__":
    unittest.main()
