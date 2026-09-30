import unittest

from core.runtime_adapter import (
    CAPABILITY_TO_ENGINE_CAPABILITIES,
    _map_capabilities_to_engine_capabilities,
    adapt_runtime,
)


class TestRuntimeAdapter(unittest.TestCase):

    def test_supported_capability_mappings(self):
        expected = {
            "knowledge": {
                "knowledge_search",
                "knowledge_retrieval",
            },
            "memory": {
                "memory_recall",
                "memory_context",
            },
            "conversation": {
                "conversation_context",
                "conversation_summary",
            },
            "reasoning": {
                "reasoning",
                "comparison",
                "recommendation",
            },
            "goals": {
                "goal_detection",
                "goal_tracking",
            },
            "planning": {
                "planning",
                "roadmap",
            },
        }

        for capability, expected_engine_capabilities in expected.items():
            with self.subTest(capability=capability):
                mapped = set(
                    _map_capabilities_to_engine_capabilities(
                        [capability]
                    )
                )
                self.assertEqual(
                    mapped,
                    expected_engine_capabilities,
                )

    def test_multiple_capabilities_are_mapped_without_duplicates(self):
        mapped = _map_capabilities_to_engine_capabilities(
            [
                "memory",
                "knowledge",
                "memory",
                "planning",
            ]
        )

        self.assertEqual(
            len(mapped),
            len(set(mapped)),
        )

        self.assertIn("memory_recall", mapped)
        self.assertIn("memory_context", mapped)
        self.assertIn("knowledge_search", mapped)
        self.assertIn("knowledge_retrieval", mapped)
        self.assertIn("planning", mapped)
        self.assertIn("roadmap", mapped)

    def test_unsupported_capabilities_are_not_invented(self):
        mapped = _map_capabilities_to_engine_capabilities(
            [
                "adaptive_intelligence",
                "governance",
                "oversight",
                "accountability",
            ]
        )

        self.assertEqual(mapped, [])

    def test_unknown_capability_is_ignored(self):
        mapped = _map_capabilities_to_engine_capabilities(
            [
                "unknown_capability",
                "memory",
            ]
        )

        self.assertEqual(
            mapped,
            [
                "memory_recall",
                "memory_context",
            ],
        )

    def test_mapping_registry_contains_only_supported_7j_capabilities(self):
        expected_capabilities = {
            "knowledge",
            "memory",
            "conversation",
            "reasoning",
            "goals",
            "planning",
        }

        self.assertEqual(
            set(CAPABILITY_TO_ENGINE_CAPABILITIES),
            expected_capabilities,
        )

    def test_memory_runtime_handoff(self):
        result = adapt_runtime(
            {
                "intent": "MEMORY_SAVE",
                "command": "remember that my favorite car is a BMW",
            }
        )

        runtime = result["runtime"]

        self.assertIn(
            "memory",
            runtime["discovered_capabilities"],
        )

        # MEMORY_SAVE must not be represented as a
        # memory recall operation in 7J.
        self.assertNotIn(
            "memory_recall",
            runtime["requested_capabilities"],
        )

        self.assertNotIn(
            "memory_context",
            runtime["requested_capabilities"],
        )

        # The actual storage action belongs to 9A-9I.
        capability_result = runtime["capability_result"]

        selected_tools = capability_result[
            "selected_tools"
        ]

        self.assertEqual(
            selected_tools[0]["tool_id"],
            "memory_store",
        )

        # 9F remains disabled.
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

    def test_knowledge_runtime_handoff(self):
        result = adapt_runtime(
            {
                "intent": "UNKNOWN",
                "command": "what is software testing",
            }
        )

        runtime = result["runtime"]

        self.assertIn(
            "knowledge",
            runtime["discovered_capabilities"],
        )

        self.assertIn(
            "knowledge_search",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "knowledge_retrieval",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "knowledge",
            runtime["selected_engines"],
        )

    def test_conversation_runtime_handoff(self):
        result = adapt_runtime(
            {
                "intent": "UNKNOWN",
                "command": "what did i say earlier",
            }
        )

        runtime = result["runtime"]

        self.assertIn(
            "conversation",
            runtime["discovered_capabilities"],
        )

        self.assertIn(
            "conversation_context",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "conversation_summary",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "context",
            runtime["selected_engines"],
        )

    def test_reasoning_runtime_handoff(self):
        result = adapt_runtime(
            {
                "intent": "UNKNOWN",
                "command": "compare python and java",
            }
        )

        runtime = result["runtime"]

        self.assertIn(
            "reasoning",
            runtime["discovered_capabilities"],
        )

        self.assertIn(
            "reasoning",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "comparison",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "recommendation",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "reasoning",
            runtime["selected_engines"],
        )

    def test_goals_runtime_handoff(self):
        result = adapt_runtime(
            {
                "intent": "UNKNOWN",
                "command": "what is my goal progress",
            }
        )

        runtime = result["runtime"]

        self.assertIn(
            "goals",
            runtime["discovered_capabilities"],
        )

        self.assertIn(
            "goal_detection",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "goal_tracking",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "goal",
            runtime["selected_engines"],
        )

    def test_planning_runtime_handoff(self):
        result = adapt_runtime(
            {
                "intent": "UNKNOWN",
                "command": "create a roadmap for learning python",
            }
        )

        runtime = result["runtime"]

        self.assertIn(
            "planning",
            runtime["discovered_capabilities"],
        )

        self.assertIn(
            "planning",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "roadmap",
            runtime["requested_capabilities"],
        )

        self.assertIn(
            "planner",
            runtime["selected_engines"],
        )

    def test_safety_boundary_remains_disabled(self):
        result = adapt_runtime(
            {
                "intent": "MEMORY_SAVE",
                "command": "remember that my favorite car is a BMW",
            }
        )

        runtime = result["runtime"]

        self.assertFalse(
            runtime["execution_enabled"]
        )

        self.assertFalse(
            runtime["automatic_action_allowed"]
        )

        self.assertFalse(
            runtime["self_modification_allowed"]
        )

        self.assertFalse(
            runtime["decision_override_allowed"]
        )


if __name__ == "__main__":
    unittest.main()
