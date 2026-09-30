"""
HOPE Workflow Planning

11C - Creates an ordered plan from a defined workflow.

This layer plans workflow execution only.
It does not execute workflow steps.
"""

from core.workflow_definition import define_workflow


LAYER = "11C"
STATUS = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def create_workflow_plan(workflow_definition):
    if not isinstance(workflow_definition, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "plan_valid": False,
            "workflow": None,
            "plan": [],
            "plan_step_count": 0,
            "execution_requested": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Workflow definition must be a dictionary.",
        }

    if workflow_definition.get("workflow_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "plan_valid": False,
            "workflow": workflow_definition,
            "plan": [],
            "plan_step_count": 0,
            "execution_requested": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Workflow definition is not valid.",
        }

    steps = workflow_definition.get("steps")

    if not isinstance(steps, list) or not steps:
        return {
            "layer": LAYER,
            "status": STATUS,
            "plan_valid": False,
            "workflow": workflow_definition,
            "plan": [],
            "plan_step_count": 0,
            "execution_requested": False,
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
            "reason": "Workflow must contain at least one step.",
        }

    plan = []

    for index, step in enumerate(steps, start=1):
        plan.append(
            {
                "plan_step": index,
                "step_id": step.get("step_id"),
                "name": step.get("name"),
                "depends_on": list(step.get("depends_on", [])),
                "status": "PLANNED",
            }
        )

    return {
        "layer": LAYER,
        "status": STATUS,
        "plan_valid": True,
        "workflow": workflow_definition,
        "workflow_id": workflow_definition.get("workflow_id"),
        "plan": plan,
        "plan_step_count": len(plan),
        "plan_status": "READY_FOR_CONTROL",
        "execution_requested": False,
        "execution_allowed": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Workflow plan prepared; execution remains disabled.",
    }


def get_workflow_planning_regression():
    workflow = define_workflow(
        "Organize my daily tasks.",
        "Daily Task Workflow",
        [
            "collect_tasks",
            "prioritize_tasks",
            "prepare_summary",
        ],
    )

    plan = create_workflow_plan(workflow)

    invalid_definition = create_workflow_plan({})
    invalid_type = create_workflow_plan(None)

    return {
        "layer": plan["layer"] == LAYER,
        "status": plan["status"] == STATUS,
        "plan_valid": plan["plan_valid"] is True,
        "workflow_id_preserved": (
            plan["workflow_id"] == workflow["workflow_id"]
        ),
        "three_plan_steps_created": plan["plan_step_count"] == 3,
        "plan_steps_are_planned": all(
            step["status"] == "PLANNED"
            for step in plan["plan"]
        ),
        "step_ids_preserved": (
            plan["plan"][0]["step_id"] == "step_1"
            and plan["plan"][1]["step_id"] == "step_2"
            and plan["plan"][2]["step_id"] == "step_3"
        ),
        "dependencies_preserved": (
            plan["plan"][1]["depends_on"] == ["step_1"]
            and plan["plan"][2]["depends_on"] == ["step_2"]
        ),
        "plan_status_ready_for_control": (
            plan["plan_status"] == "READY_FOR_CONTROL"
        ),
        "execution_not_requested": (
            plan["execution_requested"] is False
        ),
        "execution_disabled": (
            plan["execution_allowed"] is False
        ),
        "automatic_action_disabled": (
            plan["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            plan["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            plan["decision_override_allowed"] is False
        ),
        "invalid_definition_rejected": (
            invalid_definition["plan_valid"] is False
        ),
        "invalid_type_rejected": (
            invalid_type["plan_valid"] is False
        ),
    }
