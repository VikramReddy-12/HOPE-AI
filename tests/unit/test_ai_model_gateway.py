import unittest

from core.ai_model_gateway import (
    DEFAULT_MODEL,
    DEFAULT_PROVIDER,
    LAYER,
    STATUS,
    get_ai_gateway_regression,
    get_gateway_status,
    get_supported_providers,
    prepare_ai_request,
    validate_provider,
)


class TestAIModelGateway(unittest.TestCase):

    def test_gateway_layer(self):
        self.assertEqual(LAYER, "10A")
        self.assertEqual(STATUS, "READY")

    def test_default_provider_and_model(self):
        self.assertEqual(DEFAULT_PROVIDER, "openai")
        self.assertEqual(DEFAULT_MODEL, "gpt-5.6-luna")

    def test_supported_providers(self):
        providers = get_supported_providers()

        self.assertIn("openai", providers)
        self.assertIn("google", providers)
        self.assertIn("anthropic", providers)

    def test_unknown_provider_rejected(self):
        result = validate_provider("unknown_provider")

        self.assertFalse(result["valid"])
        self.assertFalse(result["configured"])

    def test_empty_prompt_rejected(self):
        result = prepare_ai_request("")

        self.assertFalse(result["request_valid"])
        self.assertFalse(result["request_allowed"])

    def test_request_is_prepared_without_execution(self):
        result = prepare_ai_request(
            "Analyze the HOPE architecture."
        )

        self.assertTrue(result["request_valid"])
        self.assertFalse(result["executed"])
        self.assertFalse(result["request_allowed"])

    def test_gateway_execution_disabled(self):
        status = get_gateway_status()

        self.assertFalse(
            status["ai_request_enabled"]
        )

    def test_automatic_action_disabled(self):
        status = get_gateway_status()

        self.assertFalse(
            status["automatic_action_allowed"]
        )

    def test_self_modification_disabled(self):
        status = get_gateway_status()

        self.assertFalse(
            status["self_modification_allowed"]
        )

    def test_decision_override_disabled(self):
        status = get_gateway_status()

        self.assertFalse(
            status["decision_override_allowed"]
        )

    def test_gateway_regression_passes(self):
        result = get_ai_gateway_regression()

        self.assertTrue(
            result["regression_passed"]
        )


if __name__ == "__main__":
    unittest.main()
