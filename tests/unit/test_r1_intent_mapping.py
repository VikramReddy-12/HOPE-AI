import unittest

from core.runtime_adapter import (
    _map_capabilities_to_engine_capabilities,
    _get_intent_aware_engine_capabilities,
    adapt_runtime,
)


class TestR1IntentAwareMapping(unittest.TestCase):

    def test_memory_save_does_not_map_to_recall(self):
        result = _get_intent_aware_engine_capabilities(
            "MEMORY_SAVE",
            ["memory"],
        )

        self.assertNotIn(
            "memory_recall",
            result,
        )

    def test_memory_save_does_not_map_to_context(self):
        result = _get_intent_aware_engine_capabilities(
            "MEMORY_SAVE",
            ["memory"],
        )

        self.assertNotIn(
            "memory_context",
            result,
        )

    def test_memory_save_has_no_7j_memory_capability(self):
        result = _get_intent_aware_engine_capabilities(
            "MEMORY_SAVE",
            ["memory"],
        )

        self.assertEqual(
            result,
            [],
        )

    def test_memory_recall_keeps_recall_mapping(self):
        result = _get_intent_aware_engine_capabilities(
            "MEMORY_RECALL",
            ["memory"],
        )

        self.assertEqual(
            result,
            [
                "memory_recall",
                "memory_context",
            ],
        )

    def test_knowledge_search_keeps_knowledge_mapping(self):
        result = _get_intent_aware_engine_capabilities(
            "KNOWLEDGE_SEARCH",
            ["knowledge"],
        )

        self.assertEqual(
            result,
            [
                "knowledge_search",
                "knowledge_retrieval",
            ],
        )

    def test_generic_mapping_remains_unchanged(self):
        result = _map_capabilities_to_engine_capabilities(
            ["memory"]
        )

        self.assertEqual(
            result,
            [
                "memory_recall",
                "memory_context",
            ],
        )

    def test_runtime_memory_save_uses_no_recall_capability(self):
        result = adapt_runtime(
            {
                "intent": "MEMORY_SAVE",
                "command": (
                    "remember that my favorite car is a BMW"
                ),
            }
        )

        runtime = result["runtime"]

        self.assertEqual(
            runtime["requested_capabilities"],
            [],
        )

        self.assertNotIn(
            "memory_recall",
            runtime["requested_capabilities"],
        )

    def test_runtime_memory_save_still_selects_memory_store(self):
        result = adapt_runtime(
            {
                "intent": "MEMORY_SAVE",
                "command": (
                    "remember that my favorite car is a BMW"
                ),
            }
        )

        capability_result = result["runtime"][
            "capability_result"
        ]

        selected_tools = capability_result[
            "selected_tools"
        ]

        self.assertEqual(
            selected_tools[0]["tool_id"],
            "memory_store",
        )

    def test_memory_store_remains_blocked(self):
        result = adapt_runtime(
            {
                "intent": "MEMORY_SAVE",
                "command": (
                    "remember that my favorite car is a BMW"
                ),
            }
        )

        capability_result = result["runtime"][
            "capability_result"
        ]

        action_result = capability_result[
            "action_results"
        ][0]

        self.assertEqual(
            action_result["result_status"],
            "HUMAN_REVIEW",
        )

        self.assertFalse(
            action_result["execution_enabled"]
        )


if __name__ == "__main__":
    unittest.main()
