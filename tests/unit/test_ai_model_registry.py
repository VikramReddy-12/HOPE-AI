import unittest

from core.ai_model_registry import (
    AUTOMATIC_ACTION_ALLOWED,
    DECISION_OVERRIDE_ALLOWED,
    LAYER,
    SELF_MODIFICATION_ALLOWED,
    STATUS,
    get_model,
    get_model_registry,
    get_model_registry_regression,
    get_model_registry_status,
    get_provider_models,
    is_model_registered,
)


class TestAIModelRegistry(unittest.TestCase):

    def test_registry_layer(self):
        self.assertEqual(LAYER, "10B")

    def test_registry_status(self):
        self.assertEqual(STATUS, "READY")

    def test_three_providers_registered(self):
        registry = get_model_registry()

        self.assertIn("openai", registry)
        self.assertIn("google", registry)
        self.assertIn("anthropic", registry)

    def test_openai_model_registered(self):
        self.assertTrue(
            is_model_registered(
                "openai",
                "gpt-5.6-luna",
            )
        )

    def test_openai_model_lookup(self):
        model = get_model(
            "openai",
            "gpt-5.6-luna",
        )

        self.assertIsNotNone(model)
        self.assertEqual(
            model["model_id"],
            "gpt-5.6-luna",
        )
        self.assertTrue(model["reasoning"])
        self.assertTrue(model["coding"])
        self.assertTrue(model["general_assistance"])
        self.assertTrue(model["tool_use"])

    def test_provider_model_lookup(self):
        models = get_provider_models("openai")

        self.assertIn(
            "gpt-5.6-luna",
            models,
        )

    def test_unknown_model_rejected(self):
        self.assertIsNone(
            get_model(
                "openai",
                "unknown_model",
            )
        )

    def test_unknown_provider_rejected(self):
        self.assertIsNone(
            get_model(
                "unknown_provider",
                "unknown_model",
            )
        )

    def test_registry_model_count(self):
        status = get_model_registry_status()

        self.assertEqual(
            status["model_count"],
            3,
        )

    def test_automatic_action_disabled(self):
        self.assertFalse(
            AUTOMATIC_ACTION_ALLOWED
        )

    def test_self_modification_disabled(self):
        self.assertFalse(
            SELF_MODIFICATION_ALLOWED
        )

    def test_decision_override_disabled(self):
        self.assertFalse(
            DECISION_OVERRIDE_ALLOWED
        )

    def test_registry_regression_passes(self):
        result = get_model_registry_regression()

        self.assertTrue(
            result["regression_passed"]
        )


if __name__ == "__main__":
    unittest.main()
