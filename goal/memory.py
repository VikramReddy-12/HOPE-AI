"""
HOPE Goal Memory

Stores and retrieves the user's
current long-term goal.
"""

_current_goal = None


def save_goal(goal):
    """
    Save the current goal.
    """

    global _current_goal

    _current_goal = goal


def get_goal():
    """
    Return the current goal.
    """

    return _current_goal


def clear_goal():
    """
    Clear the current goal.
    """

    global _current_goal

    _current_goal = None