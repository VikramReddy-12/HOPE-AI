"""
HOPE Goal Engine

Coordinates the Goal Detection Engine,
stores the user's goal using the unified
Memory Engine, and returns structured
goal information.
"""

from goal.detector import detect_goal
from memory.manager import remember


def process_goal(command):
    """
    Process a user's command and determine
    whether it contains a goal.

    Parameters:
        command (str)

    Returns:
        dict | None
    """

    # Detect the goal
    result = detect_goal(command)

    if result is None:
        return None

    goal = result["goal"]

    # Save the goal using HOPE's unified memory system
    remember("current_goal", goal)

    # Return structured goal information
    return {
        "intent": "GOAL",
        "goal": goal,
        "pattern": result["pattern"]
    }