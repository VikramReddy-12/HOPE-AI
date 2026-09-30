import unittest

from assistant.action_dispatcher import _prepare_capability_action


class TestMemorySaveControlledBoundary(unittest.TestCase):

    def test_memory_save_contains_controlled_boundary(self):
        result = _prepare_capability_action(
            {
                "intent": "MEMORY_SAVE",
                "command": "remember test_c32_dispatch hello",
            }
        )

        self.assertIn("action_dispatch", result)

        capability_result = result["action_dispatch"]

        self.assertIn(
            "controlled_execution",
            capability_result,
        )

        boundary = capability_result["controlled_execution"]

        self.assertEqual(boundary["layer"], "9F")
        self.assertEqual(boundary["tool_id"], "memory_store")

    def test_memory_save_boundary_remains_blocked(self):
        result = _prepare_capability_action(
            {
                "intent": "MEMORY_SAVE",
                "command": "remember test_c32_blocked hello",
            }
        )

        boundary = result["action_dispatch"]["controlled_execution"]

        self.assertFalse(boundary["execution_allowed"])

    def test_memory_save_does_not_execute_through_9f(self):
        result = _prepare_capability_action(
            {
                "intent": "MEMORY_SAVE",
                "command": "remember test_c32_no_execute hello",
            }
        )

        boundary = result["action_dispatch"]["controlled_execution"]

        self.assertFalse(boundary["execution_allowed"])

        self.assertEqual(
            boundary["execution_status"],
            "EXECUTION_NOT_ALLOWED",
        )


if __name__ == "__main__":
    unittest.main()
