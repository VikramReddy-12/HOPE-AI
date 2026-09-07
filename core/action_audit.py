"""
HOPE-AI 9H Action Memory / Audit

Records standardized action outcomes for auditability.

This layer:
- records action results
- preserves tool identity
- preserves result status
- preserves safety state
- provides deterministic audit records
- does not execute tools
- does not automatically modify long-term memory
"""

from datetime import datetime, timezone
from uuid import uuid4

from core.action_results import (
    get_action_result,
)


LAYER = "9H"
STATUS_READY = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


AUDIT_STORE = []


def create_audit_record(action_result):
    """
    Create a normalized audit record from a 9G action result.

    The record is stored only in the in-process audit store.
    """

    audit_id = str(uuid4())

    record = {
        "audit_id": audit_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "layer": LAYER,
        "tool_id": action_result.get("tool_id"),
        "result_status": action_result.get("result_status"),
        "success": action_result.get("success", False),
        "result": action_result.get("result"),
        "error": action_result.get("error"),
        "reason": action_result.get("reason"),
        "human_review_required": action_result.get(
            "human_review_required",
            False,
        ),
        "execution_enabled": action_result.get(
            "execution_enabled",
            False,
        ),
    }

    AUDIT_STORE.append(record)

    return record


def record_action(
    tool_id,
    input_data=None,
):
    """
    Obtain a standardized 9G action result and create its
    corresponding 9H audit record.

    Actual execution remains disabled.
    """

    action_result = get_action_result(
        tool_id,
        input_data,
    )

    audit_record = create_audit_record(
        action_result
    )

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "action_result": action_result,
        "audit_record": audit_record,
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def get_audit_records():
    """
    Return a copy of all audit records.
    """

    return list(AUDIT_STORE)


def get_audit_record(audit_id):
    """
    Retrieve one audit record by audit identifier.
    """

    for record in AUDIT_STORE:
        if record["audit_id"] == audit_id:
            return dict(record)

    return None


def clear_audit_store():
    """
    Clear the in-process audit store.

    This exists for deterministic testing and does not
    modify persistent user memory.
    """

    AUDIT_STORE.clear()


def get_action_audit_status():
    """Return the current 9H audit status."""

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "audit_available": True,
        "audit_record_count": len(AUDIT_STORE),
        "execution_enabled": EXECUTION_ENABLED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def get_action_audit_regression():
    """
    Validate the 9H Action Memory / Audit layer.
    """

    clear_audit_store()

    memory_record = record_action(
        "memory_store",
        {
            "key": "favorite_car",
            "value": "BMW 7 Series",
        },
    )

    unknown_record = record_action(
        "unknown_tool",
        {},
    )

    memory_audit = memory_record["audit_record"]
    unknown_audit = unknown_record["audit_record"]

    status = get_action_audit_status()

    checks = {
        "layer_9h": LAYER == "9H",
        "status_ready": STATUS_READY == "READY",

        "memory_audit_created": (
            memory_audit["audit_id"] != ""
        ),

        "memory_tool_preserved": (
            memory_audit["tool_id"]
            == "memory_store"
        ),

        "memory_result_preserved": (
            memory_audit["result_status"]
            == "HUMAN_REVIEW"
        ),

        "memory_review_preserved": (
            memory_audit["human_review_required"]
            is True
        ),

        "memory_not_executed": (
            memory_audit["execution_enabled"]
            is False
        ),

        "unknown_audit_created": (
            unknown_audit["audit_id"] != ""
        ),

        "unknown_tool_preserved": (
            unknown_audit["tool_id"]
            == "unknown_tool"
        ),

        "unknown_result_preserved": (
            unknown_audit["result_status"]
            == "BLOCKED"
        ),

        "records_available": (
            len(get_audit_records()) == 2
        ),

        "memory_record_retrievable": (
            get_audit_record(
                memory_audit["audit_id"]
            )
            is not None
        ),

        "unknown_record_retrievable": (
            get_audit_record(
                unknown_audit["audit_id"]
            )
            is not None
        ),

        "audit_available": (
            status["audit_available"] is True
        ),

        "execution_disabled": (
            status["execution_enabled"] is False
        ),

        "automatic_action_disabled": (
            status["automatic_action_allowed"] is False
        ),

        "self_modification_disabled": (
            status["self_modification_allowed"] is False
        ),

        "decision_override_disabled": (
            status["decision_override_allowed"] is False
        ),
    }

    return {
        "integration_layer": LAYER,
        "integration_status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "memory_record": memory_record,
        "unknown_record": unknown_record,
        "audit_records": get_audit_records(),
        "execution_enabled": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


if __name__ == "__main__":
    print("9H ACTION MEMORY / AUDIT REGRESSION:")
    print(get_action_audit_regression())
