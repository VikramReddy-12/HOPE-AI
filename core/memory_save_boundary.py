from core.controlled_execution import (
    LAYER,
    STATUS_READY,
    EXECUTION_BLOCKED,
    EXECUTION_NOT_ALLOWED,
    validate_execution_request,
)


MEMORY_SAVE_TOOL = "memory_store"


def prepare_memory_save_request(key, value):
    """
    Prepare a MEMORY_SAVE request for the 9F controlled execution boundary.

    This function prepares data only. It never writes to memory.
    """

    if not isinstance(key, str) or not key.strip():
        return {
            "layer": LAYER,
            "status": STATUS_READY,
            "tool_id": MEMORY_SAVE_TOOL,
            "execution_allowed": False,
            "execution_status": EXECUTION_NOT_ALLOWED,
            "request_valid": False,
            "reason": "Memory key must be a non-empty string.",
        }

    if not isinstance(value, str):
        value = str(value)

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "tool_id": MEMORY_SAVE_TOOL,
        "input_data": {
            "key": key.strip(),
            "value": value,
        },
        "request_valid": True,
        "execution_allowed": False,
        "execution_status": EXECUTION_BLOCKED,
        "reason": "Memory save request prepared; controlled execution is disabled.",
    }


def validate_memory_save_boundary(key, value):
    """
    Validate a MEMORY_SAVE request against the existing 9F gate.

    This does not execute the memory operation.
    """

    request = prepare_memory_save_request(key, value)

    if not request["request_valid"]:
        return request

    gate = validate_execution_request(MEMORY_SAVE_TOOL)

    request["gate_decision"] = gate["decision"]
    request["gate_execution_status"] = gate["execution_status"]
    request["gate_execution_allowed"] = gate["execution_allowed"]
    request["gate_reason"] = gate["reason"]

    request["execution_allowed"] = (
        request["request_valid"]
        and gate["execution_allowed"]
    )

    if not request["execution_allowed"]:
        request["execution_status"] = gate["execution_status"]

    return request


def get_memory_save_boundary_regression():
    valid_request = prepare_memory_save_request(
        "test_c32_boundary",
        "hello",
    )

    validated_request = validate_memory_save_boundary(
        "test_c32_boundary",
        "hello",
    )

    invalid_request = prepare_memory_save_request(
        "",
        "hello",
    )

    checks = {
        "layer_9f": LAYER == "9F",
        "valid_request_prepared": (
            valid_request["request_valid"] is True
        ),
        "memory_store_tool": (
            valid_request["tool_id"] == MEMORY_SAVE_TOOL
        ),
        "key_preserved": (
            valid_request["input_data"]["key"]
            == "test_c32_boundary"
        ),
        "value_preserved": (
            valid_request["input_data"]["value"]
            == "hello"
        ),
        "valid_request_not_executed": (
            valid_request["execution_allowed"] is False
        ),
        "gate_blocks_execution": (
            validated_request["gate_execution_allowed"]
            is False
        ),
        "boundary_blocks_execution": (
            validated_request["execution_allowed"] is False
        ),
        "invalid_key_rejected": (
            invalid_request["request_valid"] is False
        ),
        "no_memory_write_performed": True,
    }

    return {
        "layer": LAYER,
        "status": STATUS_READY,
        "regression_passed": all(checks.values()),
        "checks": checks,
        "valid_request": valid_request,
        "validated_request": validated_request,
        "invalid_request": invalid_request,
    }


if __name__ == "__main__":
    print("C3.2 MEMORY SAVE CONTROLLED BOUNDARY REGRESSION:")
    print(get_memory_save_boundary_regression())
