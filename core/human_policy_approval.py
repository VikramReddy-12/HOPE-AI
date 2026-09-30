"""
HOPE-AI 10H Human/Policy Approval

Creates an explicit approval decision for a verified AI tool intent.

This layer does not execute tools, grant unrestricted permissions,
modify the system, or override human decisions.

Approval is represented as a controlled proposal for downstream
policy handling. Actual execution remains disabled.
"""

LAYER = "10H"
STATUS = "READY"

AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False
EXECUTION_ALLOWED = False


def approve_verified_intent(verification_result, human_approval=False):
    if not isinstance(verification_result, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "approval_valid": False,
            "approval_granted": False,
            "approval_status": "REJECTED",
            "reason": "Verification result must be a dictionary.",
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    if verification_result.get("verification_passed") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "approval_valid": False,
            "approval_granted": False,
            "approval_status": "REJECTED",
            "reason": "Verified intent is required before approval.",
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    verified_intent = verification_result.get("verified_intent")

    if not isinstance(verified_intent, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "approval_valid": False,
            "approval_granted": False,
            "approval_status": "REJECTED",
            "reason": "Verified intent payload is missing or invalid.",
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    if verified_intent.get("proposed_only") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "approval_valid": False,
            "approval_granted": False,
            "approval_status": "REJECTED",
            "reason": "Only proposed intents can enter the approval boundary.",
            "execution_allowed": EXECUTION_ALLOWED,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    if human_approval is True:
        approval_status = "APPROVED"
        approval_granted = True
        reason = (
            "Human approval recorded; execution remains disabled "
            "until downstream policy and controlled execution permit it."
        )
    else:
        approval_status = "HUMAN_REVIEW_REQUIRED"
        approval_granted = False
        reason = (
            "Human approval is required before the verified intent "
            "can proceed."
        )

    return {
        "layer": LAYER,
        "status": STATUS,
        "approval_valid": True,
        "approval_granted": approval_granted,
        "approval_status": approval_status,
        "verified_intent": verified_intent,
        "human_approval": human_approval is True,
        "execution_allowed": EXECUTION_ALLOWED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": reason,
    }


def get_human_policy_approval_regression():
    valid_verification = {
        "verification_passed": True,
        "verified_intent": {
            "intent_type": "memory_save",
            "tool_id": "memory_store",
            "capability": "memory",
            "request": "Remember that my favorite car is BMW 7 Series.",
            "verified": True,
            "proposed_only": True,
        },
    }

    unapproved_result = approve_verified_intent(
        valid_verification,
        human_approval=False,
    )

    approved_result = approve_verified_intent(
        valid_verification,
        human_approval=True,
    )

    invalid_verification = approve_verified_intent({})

    invalid_payload = approve_verified_intent({
        "verification_passed": True,
        "verified_intent": None,
    })

    non_proposed_verification = approve_verified_intent({
        "verification_passed": True,
        "verified_intent": {
            "intent_type": "memory_save",
            "tool_id": "memory_store",
            "capability": "memory",
            "request": "Remember this.",
            "verified": True,
            "proposed_only": False,
        },
    })

    checks = {
        "layer_10h": LAYER == "10H",
        "status_ready": STATUS == "READY",

        "unapproved_requires_review": (
            unapproved_result["approval_status"]
            == "HUMAN_REVIEW_REQUIRED"
        ),
        "unapproved_not_granted": (
            unapproved_result["approval_granted"] is False
        ),

        "approved_status_recorded": (
            approved_result["approval_status"] == "APPROVED"
        ),
        "approved_granted": (
            approved_result["approval_granted"] is True
        ),
        "human_approval_recorded": (
            approved_result["human_approval"] is True
        ),

        "invalid_verification_rejected": (
            invalid_verification["approval_granted"] is False
        ),
        "invalid_payload_rejected": (
            invalid_payload["approval_granted"] is False
        ),
        "non_proposed_intent_rejected": (
            non_proposed_verification["approval_granted"] is False
        ),

        "execution_disabled_after_approval": (
            approved_result["execution_allowed"] is False
        ),
        "automatic_action_disabled": (
            approved_result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            approved_result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            approved_result["decision_override_allowed"] is False
        ),
    }

    return {
        "layer": LAYER,
        "status": STATUS,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "unapproved_result": unapproved_result,
        "approved_result": approved_result,
        "invalid_verification": invalid_verification,
        "invalid_payload": invalid_payload,
        "non_proposed_verification": non_proposed_verification,
    }


if __name__ == "__main__":
    print("10H HUMAN/POLICY APPROVAL REGRESSION:")
    print(get_human_policy_approval_regression())
