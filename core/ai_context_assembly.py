"""
HOPE-AI 10D AI Context Assembly

Builds a controlled context package for an AI model request.

This layer assembles context only. It does not call AI models,
execute tools, modify the system, or override human/policy decisions.
"""

LAYER = "10D"
STATUS = "READY"

AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_text(value):
    if value is None:
        return ""

    if not isinstance(value, str):
        value = str(value)

    return value.strip()


def assemble_context(
    request,
    conversation_context=None,
    memory_context=None,
    knowledge_context=None,
    reasoning_context=None,
    goal_context=None,
    adaptive_context=None,
    selected_model=None,
):
    normalized_request = _normalize_text(request)

    context = {
        "user_request": normalized_request,
        "conversation": conversation_context,
        "memory": memory_context,
        "knowledge": knowledge_context,
        "reasoning": reasoning_context,
        "goals": goal_context,
        "adaptive_intelligence": adaptive_context,
        "selected_model": selected_model,
    }

    context_sources = {
        name: value is not None
        for name, value in context.items()
        if name != "user_request"
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "request_valid": bool(normalized_request),
        "context": context,
        "context_sources": context_sources,
        "context_source_count": sum(
            context_sources.values()
        ),
        "assembly_complete": bool(normalized_request),
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_context_assembly_regression():
    result = assemble_context(
        request="Analyze the HOPE architecture.",
        conversation_context="Previous discussion about 10C.",
        memory_context={"project": "HOPE-AI"},
        knowledge_context={"topic": "AI architecture"},
        reasoning_context={"analysis": "Layered architecture"},
        goal_context={"goal": "Build HOPE AI"},
        adaptive_context={"strategy": "Incremental SDLC"},
        selected_model={
            "provider": "openai",
            "model_id": "gpt-5.6-luna",
        },
    )

    empty_result = assemble_context("")

    checks = {
        "layer_10d": LAYER == "10D",
        "status_ready": STATUS == "READY",
        "request_valid": result["request_valid"] is True,
        "assembly_complete": result["assembly_complete"] is True,
        "request_preserved": (
            result["context"]["user_request"]
            == "Analyze the HOPE architecture."
        ),
        "conversation_present": (
            result["context"]["conversation"]
            == "Previous discussion about 10C."
        ),
        "memory_present": (
            result["context"]["memory"]["project"]
            == "HOPE-AI"
        ),
        "knowledge_present": (
            result["context"]["knowledge"]["topic"]
            == "AI architecture"
        ),
        "reasoning_present": (
            result["context"]["reasoning"]["analysis"]
            == "Layered architecture"
        ),
        "goal_present": (
            result["context"]["goals"]["goal"]
            == "Build HOPE AI"
        ),
        "adaptive_context_present": (
            result["context"]["adaptive_intelligence"]["strategy"]
            == "Incremental SDLC"
        ),
        "selected_model_present": (
            result["context"]["selected_model"]["model_id"]
            == "gpt-5.6-luna"
        ),
        "context_sources_count": (
            result["context_source_count"] == 7
        ),
        "empty_request_rejected": (
            empty_result["request_valid"] is False
        ),
        "automatic_action_disabled": (
            result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            result["decision_override_allowed"] is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "assembly_result": result,
    }


if __name__ == "__main__":
    print("10D AI CONTEXT ASSEMBLY REGRESSION:")
    print(get_context_assembly_regression())
