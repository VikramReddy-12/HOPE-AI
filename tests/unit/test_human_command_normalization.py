import unittest

from core.human_command_normalization import (
    normalize_human_command,
    get_human_command_normalization_regression,
)


class TestHumanCommandNormalization(unittest.TestCase):

    def test_valid_command(self):
        result = normalize_human_command("Remember my favorite car")
        self.assertTrue(result["normalization_valid"])

    def test_empty_command(self):
        result = normalize_human_command("   ")
        self.assertFalse(result["normalization_valid"])

    def test_none_command(self):
        result = normalize_human_command(None)
        self.assertFalse(result["normalization_valid"])

    def test_whitespace_normalization(self):
        result = normalize_human_command("  hello     HOPE   ")
        self.assertEqual(result["normalized_command"], "hello HOPE")

    def test_original_command_preserved(self):
        command = "  Hello     HOPE  "
        result = normalize_human_command(command)
        self.assertEqual(result["command"], command)

    def test_length_recorded(self):
        result = normalize_human_command("Hello HOPE")
        self.assertEqual(result["command_length"], 10)

    def test_execution_disabled(self):
        result = normalize_human_command("execute something")
        self.assertFalse(result["execution_allowed"])

    def test_automatic_action_disabled(self):
        result = normalize_human_command("execute something")
        self.assertFalse(result["automatic_action_allowed"])

    def test_self_modification_disabled(self):
        result = normalize_human_command("modify yourself")
        self.assertFalse(result["self_modification_allowed"])

    def test_decision_override_disabled(self):
        result = normalize_human_command("override policy")
        self.assertFalse(result["decision_override_allowed"])

    def test_regression(self):
        regression = get_human_command_normalization_regression()
        self.assertTrue(all(regression.values()))


if __name__ == "__main__":
    unittest.main()
