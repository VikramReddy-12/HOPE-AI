"""
HOPE-AI 10I AI Decision Integration

Integrates the AI model, context, planning, tool-intent,
verification, and human/policy approval stages into one
controlled decision package.

Neutral requests that require no tool do not require model
selection or planning.

This layer does not execute tools or grant execution authority.
"""

from core.ai_model_selection import select_model
from core.ai_context_assembly import assemble_context
from core.ai_planning import create_plan
from core.ai_tool_intent import create_tool_intent
from core.ai_verification import verify_tool_intent
from core.human_policy_approval import approve_verified_intent


LAYER = "10I"
STATUS = "READY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def integrate_ai_decision(
    request,
    conversation_context=None,
    memory_context=None,
    knowledge_context=None,
    reasoning_context=None,
    goal_context=None,
    adaptive_context=None,
):
    context_package = assemble_context(
        request,
        conversation_context=conversation_context,
        memory_context=memory_context,
        knowledge_context=knowledge_context,
        reasoning_context=reasoning_context,
        goal_context=goal_context,
        adaptive_context=adaptive_context,
    )

    if context_package.get("assembly_complete") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": False,
            "decision_status": "REJECTED",
            "reason": "Context assembly failed.",
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    preliminary_tool_intent = create_tool_intent(request)

    if preliminary_tool_intent.get("intent_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": False,
            "decision_status": "REJECTED",
            "reason": "Initial tool-intent analysis failed.",
            "context_package": context_package,
            "tool_intent": preliminary_tool_intent,
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    preliminary_intent = preliminary_tool_intent.get("tool_intent", {})

    if preliminary_intent.get("tool_id") is None:
        verification = verify_tool_intent(preliminary_tool_intent)

        if verification.get("verification_passed") is not True:
            return {
                "layer": LAYER,
                "status": STATUS,
                "decision_valid": False,
                "decision_status": "REJECTED",
                "reason": "Neutral tool intent failed verification.",
                "context_package": context_package,
                "tool_intent": preliminary_tool_intent,
                "verification": verification,
                "execution_allowed": EXECUTION_ALLOWED,
                "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
                "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
                "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            }

        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": True,
            "decision_status": "NOT_REQUIRED",
            "request": request,
            "context_package": context_package,
            "model_selection": None,
            "plan": None,
            "tool_intent": preliminary_tool_intent,
            "verification": verification,
            "approval": None,
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": (
                "No tool is required; AI decision integration completed "
                "without execution."
            ),
        }

    model_selection = select_model(request)

    if model_selection.get("selection_available") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": False,
            "decision_status": "REJECTED",
            "reason": "Model selection failed.",
            "context_package": context_package,
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    selected_model = model_selection.get("selected_model")

    context_package = assemble_context(
        request,
        conversation_context=conversation_context,
        memory_context=memory_context,
        knowledge_context=knowledge_context,
        reasoning_context=reasoning_context,
        goal_context=goal_context,
        adaptive_context=adaptive_context,
        selected_model=selected_model,
    )

    plan = create_plan(context_package)

    if plan.get("plan_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": False,
            "decision_status": "REJECTED",
            "reason": "AI planning failed.",
            "context_package": context_package,
            "model_selection": model_selection,
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    tool_intent = create_tool_intent(request, plan=plan)

    if tool_intent.get("intent_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": False,
            "decision_status": "REJECTED",
            "reason": "AI tool-intent generation failed.",
            "context_package": context_package,
            "model_selection": model_selection,
            "plan": plan,
            "tool_intent": tool_intent,
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    verification = verify_tool_intent(tool_intent)

    if verification.get("verification_passed") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "decision_valid": False,
            "decision_status": "REJECTED",
            "reason": "AI tool intent failed verification.",
            "context_package": context_package,
            "model_selection": model_selection,
            "plan": plan,
            "tool_intent": tool_intent,
            "verification": verification,
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    approval = approve_verified_intent(
        verification,
        human_approval=False,
    )

    return {
        "layer": LAYER,
        "status": STATUS,
        "decision_valid": True,
        "decision_status": approval["approval_status"],
        "request": request,
        "model_selection": model_selection,
        "context_package": context_package,
        "plan": plan,
        "tool_intent": tool_intent,
        "verification": verification,
        "approval": approval,
        "execution_allowed": EXECUTION_ALLOWED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": (
            "AI decision pipeline integrated; human approval remains "
            "required and execution remains disabled."
        ),
    }


def get_ai_decision_integration_regression():
    memory_result = integrate_ai_decision(
        "Remember that my favorite car is BMW 7 Series."
    )

    knowledge_result = integrate_ai_decision(
        "What is artificial intelligence?"
    )

    neutral_result = integrate_ai_decision(
        "Hello"
    )

    invalid_result = integrate_ai_decision("")

    checks = {
        "layer_10i": LAYER == "10I",
        "status_ready": STATUS == "READY",

        "memory_decision_valid": (
            memory_result["decision_valid"] is True
        ),
        "memory_reaches_human_review": (
            memory_result["decision_status"]
            == "HUMAN_REVIEW_REQUIRED"
        ),

        "knowledge_decision_valid": (
            knowledge_result["decision_valid"] is True
        ),

        "neutral_decision_valid": (
            neutral_result["decision_valid"] is True
        ),
        "neutral_status_not_required": (
            neutral_result["decision_status"]
            == "NOT_REQUIRED"
        ),
        "neutral_no_tool": (
            neutral_result["tool_intent"]["tool_intent"]["tool_id"]
            is None
        ),
        "neutral_not_model_selected": (
            neutral_result["model_selection"] is None
        ),
        "neutral_not_planned": (
            neutral_result["plan"] is None
        ),

        "invalid_request_rejected": (
            invalid_result["decision_valid"] is False
        ),

        "execution_disabled": (
            memory_result["execution_allowed"] is False
            and knowledge_result["execution_allowed"] is False
            and neutral_result["execution_allowed"] is False
        ),

        "automatic_action_disabled": (
            memory_result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            memory_result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            memory_result["decision_override_allowed"] is False
        ),

        "approval_keeps_execution_disabled": (
            memory_result["approval"]["execution_allowed"] is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "memory_result": memory_result,
        "knowledge_result": knowledge_result,
        "neutral_result": neutral_result,
        "invalid_result": invalid_result,
    }


if __name__ == "__main__":
    print("10I AI DECISION INTEGRATION REGRESSION:")
    print(get_ai_decision_integration_regression())

