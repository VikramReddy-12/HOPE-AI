"""
HOPE Recovery Logger

Provides persistent logging and history for
HOPE automatic recovery events.

Recovery events are stored in a JSON file so
they survive HOPE restarts.
"""

import json
import os
from datetime import datetime


# ============================================================
# STORAGE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATA_DIR = os.path.join(
    BASE_DIR,
    "data"
)

HISTORY_FILE = os.path.join(
    DATA_DIR,
    "recovery_history.json"
)


# ============================================================
# INITIALIZE STORAGE
# ============================================================

def _ensure_storage():
    """
    Ensure the recovery history storage directory
    and JSON file exist.
    """

    os.makedirs(
        DATA_DIR,
        exist_ok=True
    )

    if not os.path.exists(HISTORY_FILE):

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [],
                file,
                indent=4
            )


# ============================================================
# LOAD HISTORY
# ============================================================

def _load_history():
    """
    Load recovery history from persistent storage.

    Returns:
        list: Recovery events.
    """

    _ensure_storage()

    try:

        with open(
            HISTORY_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        return []

    except (
        json.JSONDecodeError,
        OSError,
        TypeError,
    ):

        return []


# ============================================================
# SAVE HISTORY
# ============================================================

def _save_history(history):
    """
    Save recovery history to persistent storage.

    Parameters:
        history (list): Recovery events.

    Returns:
        bool: True if saved successfully.
    """

    _ensure_storage()

    try:

        with open(
            HISTORY_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                history,
                file,
                indent=4,
                ensure_ascii=False
            )

        return True

    except OSError:

        return False


# ============================================================
# LOG RECOVERY EVENT
# ============================================================

def log_recovery_event(
    module,
    failure,
    action,
    result,
    health_before,
    health_after,
):
    """
    Create and persist a recovery event.

    Parameters:
        module (str): Module name.
        failure (str): Failure state.
        action (str): Recovery action.
        result (str): Recovery result.
        health_before (str): Health before recovery.
        health_after (str): Health after recovery.

    Returns:
        dict: Recovery event.
    """

    event = {
        "time": datetime.now().strftime(
            "%d-%m-%Y %I:%M:%S %p"
        ),
        "module": module,
        "failure": failure.upper(),
        "action": action.upper(),
        "result": result.upper(),
        "health_before": health_before.upper(),
        "health_after": health_after.upper(),
    }

    history = _load_history()

    history.append(event)

    _save_history(history)

    return event


# ============================================================
# GET RECOVERY HISTORY
# ============================================================

def get_recovery_history():
    """
    Return all persisted recovery events.

    Returns:
        list: Recovery history.
    """

    return _load_history()


# ============================================================
# GET LAST RECOVERY
# ============================================================

def get_last_recovery():
    """
    Return the most recent recovery event.

    Returns:
        dict or None: Last recovery event.
    """

    history = _load_history()

    if not history:
        return None

    return history[-1]


# ============================================================
# GET RECOVERY COUNT
# ============================================================

def get_recovery_count():
    """
    Return the total number of recovery events.

    Returns:
        int: Number of recovery events.
    """

    history = _load_history()

    return len(history)


# ============================================================
# CLEAR RECOVERY HISTORY
# ============================================================

def clear_recovery_history():
    """
    Delete all stored recovery events.

    Returns:
        bool: True if history was cleared successfully.
    """

    return _save_history([])


# ============================================================
# FORMAT RECOVERY HISTORY
# ============================================================

def format_recovery_history():
    """
    Return a formatted recovery history report.

    Returns:
        str: Formatted recovery history.
    """

    history = _load_history()

    lines = [
        "📜 HOPE Recovery History",
        "",
    ]

    if not history:

        lines.append(
            "No recovery events recorded."
        )

        return "\n".join(lines)

    lines.append(
        f"Total Events: {len(history)}"
    )

    lines.append("")

    for index, event in enumerate(
        history,
        start=1
    ):

        lines.append(
            f"#{index}"
        )

        lines.append(
            f"Time    : {event.get('time', 'Unknown')}"
        )

        lines.append(
            f"Module  : {event.get('module', 'Unknown')}"
        )

        lines.append(
            f"Failure : {event.get('failure', 'Unknown')}"
        )

        lines.append(
            f"Action  : {event.get('action', 'Unknown')}"
        )

        lines.append(
            f"Result  : {event.get('result', 'Unknown')}"
        )

        lines.append(
            "Health  : "
            f"{event.get('health_before', 'Unknown')} "
            "→ "
            f"{event.get('health_after', 'Unknown')}"
        )

        lines.append("")

    return "\n".join(lines)