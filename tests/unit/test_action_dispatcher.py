import unittest

from assistant.action_dispatcher import (
    dispatch,
    get_action_dispatcher_regression,
)


class TestActionDispatcher(unittest.TestCase):

    def test_greeting_still_reaches_router(self):
        result = dispatch(
            {
                "intent": "GREETING",
                "command": "hello",
            }
        )

        self.assertEqual(result, "Hello Vikram!")

    def test_memory_save_dispatches_through_action_path(self):
        result = dispatch(
            {
                "intent": "MEMORY_SAVE",
                "command": "remember test_dispatch hello",
            }
        )

        self.assertIsInstance(result, str)

    def test_unknown_intent_keeps_legacy_router_path(self):
        result = dispatch(
            {
                "intent": "UNKNOWN",
                "command": "something unknown",
            }
        )

        self.assertIsInstance(result, str)

    def test_execution_remains_disabled(self):
        regression = get_action_dispatcher_regression()

        self.assertTrue(
            regression["checks"]["memory_execution_disabled"]
        )

        self.assertTrue(
            regression["checks"]["memory_automatic_action_disabled"]
        )

    def test_dispatcher_regression_passes(self):
        result = get_action_dispatcher_regression()

        self.assertTrue(
            result["regression_passed"]
        )


if __name__ == "__main__":
    unittest.main()
