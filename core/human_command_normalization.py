import re

LAYER = "12A"
STATUS = "READY"

EXECUTION_ENABLED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def _normalize_text(value):
    if value is None:
        return ""
    return str(value).strip()


def normalize_human_command(command):
    normalized = _normalize_text(command)

    if not normalized:
        return {
            "layer": LAYER,
            "status": STATUS,
            "normalization_valid": False,
            "command": "",
            "normalized_command": "",
            "reason": "Human command must not be empty.",
            "execution_allowed": False,
            "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
            "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
            "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        }

    normalized = re.sub(r"\s+", " ", normalized)
    normalized = normalized.strip()

    return {
        "layer": LAYER,
        "status": STATUS,
        "normalization_valid": True,
        "command": command,
        "normalized_command": normalized,
        "command_length": len(normalized),
        "execution_allowed": False,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
        "reason": "Human command normalized for downstream processing.",
    }


def get_human_command_normalization_regression():
    valid = normalize_human_command(
        "   Remember    my favorite car   is BMW 7 Series.   "
    )

    empty = normalize_human_command("   ")

    return {
        "valid_command": valid["normalization_valid"] is True,
        "whitespace_normalized": (
            valid["normalized_command"]
            == "Remember my favorite car is BMW 7 Series."
        ),
        "original_preserved": (
            valid["command"]
            == "   Remember    my favorite car   is BMW 7 Series.   "
        ),
        "length_recorded": valid["command_length"] > 0,
        "empty_rejected": empty["normalization_valid"] is False,
        "execution_disabled": valid["execution_allowed"] is False,
        "automatic_action_disabled": (
            valid["automatic_action_allowed"] is False
        ),
        "self_modification_disabled": (
            valid["self_modification_allowed"] is False
        ),
        "decision_override_disabled": (
            valid["decision_override_allowed"] is False
        ),
    }


if __name__ == "__main__":
    regression = get_human_command_normalization_regression()

    print("HOPE 12A - Human Command Normalization")
    print("-" * 50)

    for name, passed in regression.items():
        print(f"{name}: {'PASS' if passed else 'FAIL'}")

    print("-" * 50)

    if all(regression.values()):
        print("12A REGRESSION: PASS")
    else:
        print("12A REGRESSION: FAIL")
