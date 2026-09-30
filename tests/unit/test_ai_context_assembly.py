import unittest

from core.ai_context_assembly import (
    AUTOMATIC_ACTION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    LAYER,
    SELF_MODIFICATION_ALLOWED,
    STATUS,
    _normalize_text,
    assemble_context,
    get_context_assembly_regression,
)


class TestAIContextAssembly(unittest.TestCase):

    def test_context_layer(self):
        self.assertEqual(LAYER, "10D")

    def test_context_status(self):
        self.assertEqual(STATUS, "READY")

    def test_normalize_text(self):
        self.assertEqual(
            _normalize_text("  hello  "),
            "hello",
        )

    def test_none_normalizes_to_empty(self):
        self.assertEqual(
            _normalize_text(None),
            "",
        )

    def test_request_is_preserved(self):
        result = assemble_context("Analyze HOPE.")

        self.assertEqual(
            result["context"]["user_request"],
            "Analyze HOPE.",
        )

    def test_conversation_context_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            conversation_context="Previous discussion.",
        )

        self.assertEqual(
            result["context"]["conversation"],
            "Previous discussion.",
        )

    def test_memory_context_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            memory_context={"project": "HOPE-AI"},
        )

        self.assertEqual(
            result["context"]["memory"]["project"],
            "HOPE-AI",
        )

    def test_knowledge_context_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            knowledge_context={"topic": "AI"},
        )

        self.assertEqual(
            result["context"]["knowledge"]["topic"],
            "AI",
        )

    def test_reasoning_context_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            reasoning_context={"analysis": "Layered"},
        )

        self.assertEqual(
            result["context"]["reasoning"]["analysis"],
            "Layered",
        )

    def test_goal_context_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            goal_context={"goal": "Build HOPE"},
        )

        self.assertEqual(
            result["context"]["goals"]["goal"],
            "Build HOPE",
        )

    def test_adaptive_context_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            adaptive_context={"strategy": "Incremental"},
        )

        self.assertEqual(
            result["context"]["adaptive_intelligence"]["strategy"],
            "Incremental",
        )

    def test_selected_model_is_preserved(self):
        result = assemble_context(
            "Analyze HOPE.",
            selected_model={
                "provider": "openai",
                "model_id": "gpt-5.6-luna",
            },
        )

        self.assertEqual(
            result["context"]["selected_model"]["model_id"],
            "gpt-5.6-luna",
        )

    def test_context_source_count(self):
        result = assemble_context(
            "Analyze HOPE.",
            conversation_context="Conversation",
            memory_context={},
            knowledge_context={},
            reasoning_context={},
            goal_context={},
            adaptive_context={},
            selected_model={},
        )

        self.assertEqual(
            result["context_source_count"],
            7,
        )

    def test_empty_request_rejected(self):
        result = assemble_context("")

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["assembly_complete"])

    def test_automatic_action_disabled(self):
        self.assertFalse(AUTOMATIC_ACTION_ALLOWED)

    def test_self_modification_disabled(self):
        self.assertFalse(SELF_MODIFICATION_ALLOWED)

    def test_decision_override_disabled(self):
        self.assertFalse(DECISION_OVERRIDE_ALLOWED)

    def test_context_regression_passes(self):
        result = get_context_assembly_regression()

        self.assertTrue(result["regression_passed"])


if __name__ == "__main__":
    unittest.main()
