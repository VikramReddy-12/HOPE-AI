from core.controlled_execution import validate_execution_request

LAYER = "11D"
STATUS = "READY"
EXECUTION_OWNER = "9F"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def evaluate_step_execution(step):
    if not isinstance(step, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": False,
            "control_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Workflow step must be a dictionary.",
        }

    step_id = _normalize_text(step.get("step_id"))
    name = _normalize_text(step.get("name"))
    tool_id = _normalize_text(step.get("tool_id"))

    if not step_id:
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": False,
            "control_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Workflow step is missing step_id.",
        }

    if not name:
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": False,
            "control_status": "REJECTED",
            "step_id": step_id,
            "execution_allowed": False,
            "reason": "Workflow step is missing name.",
        }

    if not tool_id:
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": True,
            "control_status": "BLOCKED",
            "step_id": step_id,
            "name": name,
            "tool_id": None,
            "execution_owner": EXECUTION_OWNER,
            "policy_checked": True,
            "safety_checked": True,
            "execution_gate_checked": False,
            "execution_allowed": False,
            "reason": "No executable tool is assigned to this workflow step.",
        }

    gate = validate_execution_request(tool_id)

    return {
        "layer": LAYER,
        "status": STATUS,
        "control_valid": True,
        "control_status": "BLOCKED",
        "step_id": step_id,
        "name": name,
        "tool_id": tool_id,
        "execution_owner": EXECUTION_OWNER,
        "policy_checked": True,
        "safety_checked": True,
        "execution_gate_checked": True,
        "gate_decision": gate.get("decision"),
        "gate_execution_status": gate.get("execution_status"),
        "gate_execution_allowed": gate.get("execution_allowed", False),
        "execution_allowed": False,
        "reason": "Step execution remains blocked by the controlled execution boundary.",
    }


def create_execution_control(workflow_plan):
    if not isinstance(workflow_plan, dict):
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": False,
            "control_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Workflow plan must be a dictionary.",
        }

    if workflow_plan.get("plan_valid") is not True:
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": False,
            "control_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Workflow plan validation failed.",
        }

    plan = workflow_plan.get("plan")

    if not isinstance(plan, list) or not plan:
        return {
            "layer": LAYER,
            "status": STATUS,
            "control_valid": False,
            "control_status": "REJECTED",
            "execution_allowed": False,
            "reason": "Workflow plan must contain at least one step.",
        }

    controls = [evaluate_step_execution(step) for step in plan]

    return {
        "layer": LAYER,
        "status": STATUS,
        "control_valid": True,
        "control_status": "READY",
        "workflow_id": workflow_plan.get("workflow_id"),
        "controls": controls,
        "control_step_count": len(controls),
        "execution_owner": EXECUTION_OWNER,
        "execution_requested": False,
        "execution_allowed": False,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Workflow steps are controlled and remain blocked pending the 9F execution boundary.",
    }


def get_workflow_execution_control_regression():
    valid_plan = {
        "plan_valid": True,
        "workflow_id": "workflow_11b_001",
        "plan": [
            {
                "plan_step": 1,
                "step_id": "step_1",
                "name": "understand_request",
                "depends_on": [],
                "status": "PLANNED",
            },
            {
                "plan_step": 2,
                "step_id": "step_2",
                "name": "prepare_execution",
                "depends_on": ["step_1"],
                "status": "PLANNED",
            },
        ],
    }

    result = create_execution_control(valid_plan)

    return {
        "valid_plan_controlled": result["control_valid"] is True,
        "correct_layer": result["layer"] == LAYER,
        "correct_owner": result["execution_owner"] == EXECUTION_OWNER,
        "correct_step_count": result["control_step_count"] == 2,
        "all_steps_blocked": all(
            control.get("execution_allowed") is False
            for control in result["controls"]
        ),
        "execution_disabled": result["execution_allowed"] is False,
        "automatic_action_disabled": result["automatic_action_allowed"] is False,
        "self_modification_disabled": result["self_modification_allowed"] is False,
        "decision_override_disabled": result["decision_override_allowed"] is False,
        "invalid_plan_rejected": create_execution_control({})["control_valid"] is False,
    }


if __name__ == "__main__":
    regression = get_workflow_execution_control_regression()

    print("HOPE 11D - Step Execution Control")
    print("-" * 45)

    for name, passed in regression.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("-" * 45)

    if all(regression.values()):
        print("11D REGRESSION: PASS")
    else:
        print("11D REGRESSION: FAIL")
