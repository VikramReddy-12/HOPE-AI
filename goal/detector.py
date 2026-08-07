"""
HOPE Goal Detection Engine

Detects user goals from natural language.

Examples:
- I want to become an AI Engineer
- I want to learn Python
- My goal is to become a Data Scientist
"""

GOAL_PATTERNS = [
    "i want to become",
    "i want to be",
    "my goal is",
    "i want to learn",
    "i want a job as",
    "i want a career in",
    "i would like to become",
]


def detect_goal(command):
    """
    Detects a goal from the user's command.

    Parameters:
        command (str)

    Returns:
        dict | None
    """

    command = command.lower().strip()

    for pattern in GOAL_PATTERNS:

        if command.startswith(pattern):

            goal = command.replace(pattern, "").strip()

            if goal:

                return {
                    "goal": goal.title(),
                    "pattern": pattern
                }

    return None