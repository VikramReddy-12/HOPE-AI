"""
HOPE AI - Human Command Interpretation
"""

_COMMAND_TYPES = {
    "MEMORY",
    "KNOWLEDGE",
    "REASONING",
    "PLANNING",
    "AUTOMATION",
    "CONVERSATION",
    "GENERAL",
}


def _classify_command(command: str) -> tuple[str, float]:
    text = command.strip().lower()

    if any(keyword in text for keyword in (
        "remember",
        "memorize",
        "save this",
        "save my",
        "store this",
        "store my",
        "forget",
        "recall",
        "my favorite",
    )):
        return "MEMORY", 0.95

    if any(keyword in text for keyword in (
        "what is",
        "what are",
        "who is",
        "who are",
        "where is",
        "when is",
        "why is",
        "explain",
        "tell me about",
        "define",
    )):
        return "KNOWLEDGE", 0.95

    if any(keyword in text for keyword in (
        "analyze",
        "analyse",
        "reason",
        "solve",
        "calculate",
        "compare",
        "evaluate",
        "figure out",
        "find out",
        "why does",
    )):
        return "REASONING", 0.90

    if any(keyword in text for keyword in (
        "create a plan",
        "make a plan",
        "study plan",
        "plan this",
        "plan my",
        "schedule",
        "roadmap",
        "strategy",
    )):
        return "PLANNING", 0.95

    if any(keyword in text for keyword in (
        "automate",
        "automation",
        "automatically",
    )):
        return "AUTOMATION", 0.95

    if any(
        text == keyword or text.startswith(keyword + " ")
        for keyword in (
            "hello",
            "hi",
            "hey",
            "good morning",
            "good afternoon",
            "good evening",
            "how are you",
            "thanks",
            "thank you",
        )
    ):
        return "CONVERSATION", 0.90

    return "GENERAL", 0.75


def interpret_human_command(command):
    if command is None or not isinstance(command, str) or not command.strip():
        return {
            "interpretation_valid": False,
            "command_type": None,
            "interpretation_confidence": 0.0,
            "interpretation_only": True,
            "execution_allowed": False,
            "automatic_action_allowed": False,
            "self_modification_allowed": False,
            "decision_override_allowed": False,
        }

    command_type, confidence = _classify_command(command)

    return {
        "interpretation_valid": True,
        "command_type": command_type,
        "interpretation_confidence": confidence,
        "interpretation_only": True,
        "execution_allowed": False,
        "automatic_action_allowed": False,
        "self_modification_allowed": False,
        "decision_override_allowed": False,
    }


def get_human_command_interpretation_regression():
    tests = {
        "memory": interpret_human_command(
            "Remember my favorite car"
        )["command_type"] == "MEMORY",

        "knowledge": interpret_human_command(
            "What is Java?"
        )["command_type"] == "KNOWLEDGE",

        "reasoning": interpret_human_command(
            "Analyze this problem"
        )["command_type"] == "REASONING",

        "planning": interpret_human_command(
            "Create a study plan"
        )["command_type"] == "PLANNING",

        "automation": interpret_human_command(
            "Automate this workflow"
        )["command_type"] == "AUTOMATION",

        "conversation": interpret_human_command(
            "Hello HOPE"
        )["command_type"] == "CONVERSATION",

        "general": interpret_human_command(
            "Open my project"
        )["command_type"] == "GENERAL",

        "empty": (
            interpret_human_command("")["interpretation_valid"] is False
        ),

        "none": (
            interpret_human_command(None)["interpretation_valid"] is False
        ),

        "interpretation_only": (
            interpret_human_command("Remember this")[
                "interpretation_only"
            ] is True
        ),

        "execution_disabled": (
            interpret_human_command("Run this")[
                "execution_allowed"
            ] is False
        ),

        "automatic_action_disabled": (
            interpret_human_command("Automate this")[
                "automatic_action_allowed"
            ] is False
        ),

        "self_modification_disabled": (
            interpret_human_command("Modify yourself")[
                "self_modification_allowed"
            ] is False
        ),

        "decision_override_disabled": (
            interpret_human_command("Override policy")[
                "decision_override_allowed"
            ] is False
        ),
    }

    return tests
