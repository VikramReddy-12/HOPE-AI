import unittest

from core.human_command_interpretation import (
    interpret_human_command,
    get_human_command_interpretation_regression,
)


class TestHumanCommandInterpretation(unittest.TestCase):

    def test_memory_command(self):
        result = interpret_human_command("Remember my favorite car")
        self.assertTrue(result["interpretation_valid"])
        self.assertEqual(result["command_type"], "MEMORY")

    def test_knowledge_command(self):
        result = interpret_human_command("What is Java?")
        self.assertEqual(result["command_type"], "KNOWLEDGE")

    def test_reasoning_command(self):
        result = interpret_human_command("Analyze this problem")
        self.assertEqual(result["command_type"], "REASONING")

    def test_planning_command(self):
        result = interpret_human_command("Create a study plan")
        self.assertEqual(result["command_type"], "PLANNING")

    def test_automation_command(self):
        result = interpret_human_command("Automate this workflow")
        self.assertEqual(result["command_type"], "AUTOMATION")

    def test_conversation_command(self):
        result = interpret_human_command("Hello HOPE")
        self.assertEqual(result["command_type"], "CONVERSATION")

    def test_general_command(self):
        result = interpret_human_command("Open my project")
        self.assertEqual(result["command_type"], "GENERAL")

    def test_empty_command(self):
        result = interpret_human_command("")
        self.assertFalse(result["interpretation_valid"])

    def test_none_command(self):
        result = interpret_human_command(None)
        self.assertFalse(result["interpretation_valid"])

    def test_interpretation_only(self):
        result = interpret_human_command("Remember this")
        self.assertTrue(result["interpretation_only"])

    def test_execution_disabled(self):
        result = interpret_human_command("Run this")
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = interpret_human_command("Automate this")
        self.assertFalse(result["automatic_action_allowed"])

    def test_self_modification_disabled(self):
        result = interpret_human_command("Modify yourself")
        self.assertFalse(result["self_modification_allowed"])

    def test_decision_override_disabled(self):
        result = interpret_human_command("Override policy")
        self.assertFalse(result["decision_override_allowed"])

    def test_confidence_present(self):
        result = interpret_human_command("What is Java?")
        self.assertGreater(result["interpretation_confidence"], 0)

    def test_regression(self):
        regression = get_human_command_interpretation_regression()
        self.assertTrue(all(regression.values()))


if __name__ == "__main__":
    unittest.main()
