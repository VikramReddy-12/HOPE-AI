"""
HOPE-AI 10B AI Model Registry

Central registry describing AI providers and models available to HOPE.

This layer only stores model metadata and availability information.
It does not select models, call models, execute tools, modify the system,
or override human/policy decisions.
"""

import os


LAYER = "10B"
STATUS = "READY"

AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


MODEL_REGISTRY = {
    "openai": {
        "provider_name": "OpenAI",
        "api_key_environment": "OPENAI_API_KEY",
        "models": {
            "gpt-5.6-luna": {
                "model_id": "gpt-5.6-luna",
                "display_name": "GPT-5.6 Luna",
                "reasoning": True,
                "coding": True,
                "general_assistance": True,
                "tool_use": True,
                "availability": "registered",
            },
        },
    },
    "google": {
        "provider_name": "Google Gemini",
        "api_key_environment": "GEMINI_API_KEY",
        "models": {
            "gemini": {
                "model_id": "gemini",
                "display_name": "Google Gemini",
                "reasoning": True,
                "coding": True,
                "general_assistance": True,
                "tool_use": True,
                "availability": "registered",
            },
        },
    },
    "anthropic": {
        "provider_name": "Anthropic Claude",
        "api_key_environment": "ANTHROPIC_API_KEY",
        "models": {
            "claude": {
                "model_id": "claude",
                "display_name": "Anthropic Claude",
                "reasoning": True,
                "coding": True,
                "general_assistance": True,
                "tool_use": True,
                "availability": "registered",
            },
        },
    },
}


def _provider_configured(provider):
    provider_data = MODEL_REGISTRY.get(provider)

    if provider_data is None:
        return False

    return bool(
        os.getenv(
            provider_data["api_key_environment"],
            "",
        ).strip()
    )


def get_model_registry():
    registry = {}

    for provider, provider_data in MODEL_REGISTRY.items():
        registry[provider] = {
            "provider_name": provider_data["provider_name"],
            "api_key_environment": provider_data["api_key_environment"],
            "configured": _provider_configured(provider),
            "models": {
                model_id: dict(model_data)
                for model_id, model_data in provider_data["models"].items()
            },
        }

    return registry


def get_provider_models(provider):
    provider_data = MODEL_REGISTRY.get(provider)

    if provider_data is None:
        return {}

    return {
        model_id: dict(model_data)
        for model_id, model_data in provider_data["models"].items()
    }


def get_model(provider, model_id):
    provider_data = MODEL_REGISTRY.get(provider)

    if provider_data is None:
        return None

    model = provider_data["models"].get(model_id)

    if model is None:
        return None

    return dict(model)


def is_model_registered(provider, model_id):
    return get_model(provider, model_id) is not None


def get_model_registry_status():
    return {
        "layer": LAYER,
        "status": STATUS,
        "providers": list(MODEL_REGISTRY.keys()),
        "model_count": sum(
            len(provider_data["models"])
            for provider_data in MODEL_REGISTRY.values()
        ),
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_model_registry_regression():
    registry = get_model_registry()
    status = get_model_registry_status()

    checks = {
        "layer_10b": LAYER == "10B",
        "status_ready": STATUS == "READY",
        "openai_registered": "openai" in registry,
        "google_registered": "google" in registry,
        "anthropic_registered": "anthropic" in registry,
        "openai_model_registered": (
            is_model_registered("openai", "gpt-5.6-luna")
        ),
        "model_lookup_works": (
            get_model("openai", "gpt-5.6-luna") is not None
        ),
        "provider_lookup_works": (
            len(get_provider_models("openai")) >= 1
        ),
        "model_count_valid": status["model_count"] >= 3,
        "automatic_action_disabled": (
            status["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            status["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            status["decision_override_allowed"] is False
        ),
        "unknown_model_rejected": (
            get_model("openai", "unknown_model") is None
        ),
        "unknown_provider_rejected": (
            get_model("unknown_provider", "unknown_model") is None
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "registry_status": status,
    }


if __name__ == "__main__":
    print("10B AI MODEL REGISTRY REGRESSION:")
    print(get_model_registry_regression())
