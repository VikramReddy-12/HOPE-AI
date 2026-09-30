"""
HOPE Automation Engine

11A - Automation Engine Architecture.

Creates controlled automation workflow structures without executing actions.
Execution remains owned by the 9F controlled execution boundary.
"""

LAYER = "11A"
STATUS = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_request(request):
    if request is None:
        return ""
    return str(request).strip()


def create_automation(request):
    normalized_request = _normalize_request(request)

    if not normalized_request:
        return {
            "layer": LAYER,
            "status": STATUS,
            "request": "",
            "automation_valid": False,
            "workflow": [],
            "workflow_step_count": 0,
            "execution_requested": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Automation request must be a non-empty string.",
        }

    workflow = [
        {
            "step": 1,
            "stage": "understand_request",
            "status": "PROPOSED",
        },
        {
            "step": 2,
            "stage": "define_workflow",
            "status": "PROPOSED",
        },
        {
            "step": 3,
            "stage": "prepare_execution",
            "status": "PROPOSED",
        },
        {
            "step": 4,
            "stage": "await_controlled_execution",
            "status": "BLOCKED",
        },
    ]

    return {
        "layer": LAYER,
        "status": STATUS,
        "request": normalized_request,
        "automation_valid": True,
        "workflow": workflow,
        "workflow_step_count": len(workflow),
        "execution_requested": False,
        "execution_allowed": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Automation workflow prepared; execution remains disabled.",
    }


def get_automation_engine_regression():
    valid = create_automation("Create a workflow to organize my tasks.")
    invalid = create_automation("")

    return {
        "layer": LAYER,
        "status": STATUS,
        "valid_request": valid["automation_valid"] is True,
        "workflow_created": len(valid["workflow"]) == 4,
        "workflow_steps": valid["workflow_step_count"] == 4,
        "first_step_proposed": valid["workflow"][0]["status"] == "PROPOSED",
        "execution_step_blocked": valid["workflow"][3]["status"] == "BLOCKED",
        "invalid_request_rejected": invalid["automation_valid"] is False,
        "execution_disabled": valid["execution_allowed"] is False,
        "automatic_action_disabled": valid["automatic_action_allowed"] is False,
        "self_modification_disabled": valid["self_modification_allowed"] is False,
        "decision_override_disabled": valid["decision_override_allowed"] is False,
    }
