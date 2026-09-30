"""
HOPE-AI 10A AI Model Gateway

Provider-neutral gateway for connecting HOPE to external AI models.

External model execution is available only when explicitly enabled through
the HOPE_ENABLE_AI_REQUESTS environment variable.
Automatic actions, self-modification, and decision overrides remain disabled.
"""

import os

from openai import OpenAI

LAYER = "10A"
STATUS = "READY"
DEFAULT_PROVIDER = "openai"
DEFAULT_MODEL = "gpt-5.6-luna"

AI_REQUEST_ENABLED = (
    os.getenv("HOPE_ENABLE_AI_REQUESTS", "").strip().lower()
    in {"1", "true", "yes", "on"}
)

AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False

SUPPORTED_PROVIDERS = {
    "openai": {
        "name": "OpenAI",
        "api_key_environment": "OPENAI_API_KEY",
        "configured": False,
    },
    "google": {
        "name": "Google Gemini",
        "api_key_environment": "GEMINI_API_KEY",
        "configured": False,
    },
    "anthropic": {
        "name": "Anthropic Claude",
        "api_key_environment": "ANTHROPIC_API_KEY",
        "configured": False,
    },
}


def _is_provider_configured(provider):
    provider_data = SUPPORTED_PROVIDERS.get(provider)

    if provider_data is None:
        return False

    return bool(
        os.getenv(provider_data["api_key_environment"], "").strip()
    )


def get_supported_providers():
    providers = {}

    for provider, data in SUPPORTED_PROVIDERS.items():
        providers[provider] = {
            "name": data["name"],
            "api_key_environment": data["api_key_environment"],
            "configured": _is_provider_configured(provider),
        }

    return providers


def get_gateway_status():
    return {
        "layer": LAYER,
        "status": STATUS,
        "default_provider": DEFAULT_PROVIDER,
        "default_model": DEFAULT_MODEL,
        "ai_request_enabled": AI_REQUEST_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "providers": get_supported_providers(),
    }


def validate_provider(provider):
    if provider not in SUPPORTED_PROVIDERS:
        return {
            "provider": provider,
            "valid": False,
            "configured": False,
            "reason": "Provider is not registered.",
        }

    configured = _is_provider_configured(provider)

    return {
        "provider": provider,
        "valid": True,
        "configured": configured,
        "reason": (
            "Provider is configured."
            if configured
            else "Provider API key is not configured."
        ),
    }


def prepare_ai_request(
    prompt,
    provider=DEFAULT_PROVIDER,
    model=DEFAULT_MODEL,
):
    if not isinstance(prompt, str) or not prompt.strip():
        return {
            "layer": LAYER,
            "status": STATUS,
            "request_valid": False,
            "request_allowed": False,
            "executed": False,
            "reason": "Prompt must be a non-empty string.",
        }

    provider_result = validate_provider(provider)

    return {
        "layer": LAYER,
        "status": STATUS,
        "provider": provider,
        "model": model,
        "prompt": prompt.strip(),
        "request_valid": True,
        "provider_valid": provider_result["valid"],
        "provider_configured": provider_result["configured"],
        "request_allowed": (
            AI_REQUEST_ENABLED
            and provider_result["valid"]
            and provider_result["configured"]
            and provider == "openai"
        ),
        "executed": False,
        "reason": (
            "AI request is enabled and ready."
            if (
                AI_REQUEST_ENABLED
                and provider_result["valid"]
                and provider_result["configured"]
                and provider == "openai"
            )
            else "AI request is prepared but external model execution is disabled."
        ),
    }


def request_ai_model(
    prompt,
    provider=DEFAULT_PROVIDER,
    model=DEFAULT_MODEL,
):
    request = prepare_ai_request(prompt, provider, model)

    if not request["request_valid"]:
        return request

    if not request["provider_valid"]:
        request["reason"] = "Requested provider is not registered."
        return request

    if not request["provider_configured"]:
        request["reason"] = "Requested provider API key is not configured."
        return request

    if provider != "openai":
        request["reason"] = (
            "Only the OpenAI provider is connected in 10A."
        )
        return request

    if not AI_REQUEST_ENABLED:
        request["reason"] = (
            "External AI execution is disabled. "
            "Set HOPE_ENABLE_AI_REQUESTS=1 for an explicit live request."
        )
        return request

    try:
        client = OpenAI()

        response = client.responses.create(
            model=model,
            input=prompt.strip(),
        )

        request["executed"] = True
        request["request_allowed"] = True
        request["response_text"] = response.output_text
        request["reason"] = "OpenAI model request completed."

        return request

    except Exception as exc:
        request["executed"] = False
        request["request_allowed"] = True
        request["error_type"] = type(exc).__name__
        request["error"] = str(exc)
        request["reason"] = "OpenAI model request failed."

        return request


def get_ai_gateway_regression():
    status = get_gateway_status()

    request = prepare_ai_request(
        "Analyze the current HOPE architecture."
    )

    unknown_provider = validate_provider("unknown_provider")

    checks = {
        "layer_10a": LAYER == "10A",
        "status_ready": STATUS == "READY",
        "openai_registered": "openai" in SUPPORTED_PROVIDERS,
        "google_registered": "google" in SUPPORTED_PROVIDERS,
        "anthropic_registered": "anthropic" in SUPPORTED_PROVIDERS,
        "request_prepared": request["request_valid"] is True,
        "automatic_action_disabled": (
            status["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            status["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            status["decision_override_allowed"] is False
        ),
        "unknown_provider_rejected": (
            unknown_provider["valid"] is False
        ),
    }

    if not AI_REQUEST_ENABLED:
        checks["request_disabled_by_default"] = (
            request["request_allowed"] is False
        )

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "gateway_status": status,
        "prepared_request": request,
    }


if __name__ == "__main__":
    print("10A AI MODEL GATEWAY REGRESSION:")
    print(get_ai_gateway_regression())
