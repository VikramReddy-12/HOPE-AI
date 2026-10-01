"""
HOPE-AI Development Workflow

Controlled development workflow integration.

This module connects development requests to the existing
9A-9F and 11A-11I architecture.

Execution remains disabled.
"""

from core.automation_engine import create_automation
from core.workflow_definition import define_workflow
from core.workflow_planning import create_workflow_plan
from core.workflow_execution_control import create_execution_control
from core.tool_selection import select_tools


LAYER = "DEV-WORKFLOW"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def create_development_workflow(request):
    """
    Create a controlled development workflow for a request.

    This function prepares the workflow only.
    It does not execute the selected development tool.
    """

    selection = select_tools(request)

    selected_tools = selection["selected_tools"]

    development_tool = None

    for tool in selected_tools:
        if tool["tool_id"] == "project_inspect":
            development_tool = tool
            break

    if development_tool is None:
        return {
            "workflow_valid": False,
            "request": request,
            "reason": "No project_inspect development tool was selected.",
            "execution_allowed": False,
        }

    automation = create_automation(request)

    workflow = define_workflow(
        request,
        name="HOPE Development Workflow",
        steps=["project_inspect"],
    )

    workflow["steps"][0]["tool_id"] = development_tool["tool_id"]

    plan = create_workflow_plan(workflow)

    plan["plan"][0]["tool_id"] = development_tool["tool_id"]

    control_package = create_execution_control(plan)

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "request": request,
        "selected_tool": development_tool,
        "automation": automation,
        "workflow": workflow,
        "plan": plan,
        "control_package": control_package,
        "execution_enabled": False,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
        "workflow_valid": (
            workflow["workflow_valid"]
            and plan["plan_valid"]
            and control_package["control_valid"]
        ),
    }


def get_development_workflow_regression():
    """Validate the controlled development workflow integration."""

    result = create_development_workflow(
        "Inspect the project."
    )

    control_package = result.get("control_package", {})

    checks = {
        "layer_ready": (
            LAYER == "DEV-WORKFLOW"
            and STATUS_READY == "READY"
        ),
        "workflow_valid": result["workflow_valid"],
        "project_inspect_selected": (
            result["selected_tool"]["tool_id"]
            == "project_inspect"
        ),
        "execution_owner_is_9f": (
            control_package.get("execution_owner") == "9F"
        ),
        "execution_disabled": (
            result["execution_enabled"] is False
            and result["execution_allowed"] is False
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
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "execution_enabled": False,
    }


if __name__ == "__main__":
    print("DEVELOPMENT WORKFLOW REGRESSION:")
    print(get_development_workflow_regression())
