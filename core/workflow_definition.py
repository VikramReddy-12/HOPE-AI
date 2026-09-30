"""
HOPE Workflow Definition

11B - Defines structured workflows for the automation architecture.

This layer defines workflow structure only.
It does not execute workflow steps.
"""

LAYER = "11B"
STATUS = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def define_workflow(request, name="HOPE Workflow", steps=None):
    normalized_request = _normalize_text(request)
    normalized_name = _normalize_text(name)

    if not normalized_request:
        return {
            "layer": LAYER,
            "status": STATUS,
            "workflow_valid": False,
            "workflow_id": None,
            "name": normalized_name,
            "request": "",
            "steps": [],
            "dependencies": [],
            "workflow_status": "REJECTED",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Workflow request must be a non-empty string.",
        }

    if not normalized_name:
        normalized_name = "HOPE Workflow"

    if steps is None:
        normalized_steps = [
            {
                "step_id": "step_1",
                "name": "understand_request",
                "status": "PROPOSED",
                "depends_on": [],
            }
        ]
    elif isinstance(steps, list):
        normalized_steps = []
        for index, step in enumerate(steps, start=1):
            if isinstance(step, dict):
                step_name = _normalize_text(step.get("name"))
            else:
                step_name = _normalize_text(step)

            if not step_name:
                step_name = f"step_{index}"

            dependencies = [] if index == 1 else [f"step_{index - 1}"]

            normalized_steps.append(
                {
                    "step_id": f"step_{index}",
                    "name": step_name,
                    "status": "PROPOSED",
                    "depends_on": dependencies,
                }
            )

        if not normalized_steps:
            normalized_steps = [
                {
                    "step_id": "step_1",
                    "name": "understand_request",
                    "status": "PROPOSED",
                    "depends_on": [],
                }
            ]
    else:
        return {
            "layer": LAYER,
            "status": STATUS,
            "workflow_valid": False,
            "workflow_id": None,
            "name": normalized_name,
            "request": normalized_request,
            "steps": [],
            "dependencies": [],
            "workflow_status": "REJECTED",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Workflow steps must be provided as a list.",
        }

    dependencies = [
        {
            "step_id": step["step_id"],
            "depends_on": list(step["depends_on"]),
        }
        for step in normalized_steps
    ]

    return {
        "layer": LAYER,
        "status": STATUS,
        "workflow_valid": True,
        "workflow_id": "workflow_11b_001",
        "name": normalized_name,
        "request": normalized_request,
        "steps": normalized_steps,
        "step_count": len(normalized_steps),
        "dependencies": dependencies,
        "workflow_status": "PROPOSED",
        "execution_requested": False,
        "execution_allowed": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Workflow definition prepared; execution remains disabled.",
    }


def get_workflow_definition_regression():
    result = define_workflow(
        "Organize my daily tasks.",
        "Daily Task Workflow",
        ["collect_tasks", "prioritize_tasks", "prepare_summary"],
    )

    invalid_request = define_workflow("")
    invalid_steps = define_workflow("Test workflow", steps="invalid")

    return {
        "layer": result["layer"] == LAYER,
        "status": result["status"] == STATUS,
        "workflow_valid": result["workflow_valid"] is True,
        "workflow_id_present": bool(result["workflow_id"]),
        "name_preserved": result["name"] == "Daily Task Workflow",
        "request_preserved": result["request"] == "Organize my daily tasks.",
        "three_steps_created": result["step_count"] == 3,
        "steps_are_proposed": all(
            step["status"] == "PROPOSED"
            for step in result["steps"]
        ),
        "dependencies_created": len(result["dependencies"]) == 3,
        "workflow_status_proposed": result["workflow_status"] == "PROPOSED",
        "execution_disabled": result["execution_allowed"] is False,
        "automatic_action_disabled": (
            result["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            result["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            result["decision_override_allowed"] is False
        ),
        "invalid_request_rejected": (
            invalid_request["workflow_valid"] is False
        ),
        "invalid_steps_rejected": (
            invalid_steps["workflow_valid"] is False
        ),
    }
