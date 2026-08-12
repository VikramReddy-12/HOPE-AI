"""
HOPE Module Registry

Central registry for all HOPE engines and modules.

This module provides a single source of truth for
the components loaded by HOPE.

It also provides dynamic module state management
for the Failure Detection & Recovery system.
"""


# ============================================================
# HOPE MODULES
# ============================================================

MODULES = [

    {
        "name": "Brain Engine",
        "key": "brain",
        "status": "active",
        "description": (
            "Processes user input and coordinates "
            "intent detection."
        ),
    },

    {
        "name": "Knowledge Engine",
        "key": "knowledge",
        "status": "active",
        "description": (
            "Provides structured knowledge and "
            "topic information."
        ),
    },

    {
        "name": "Memory Engine",
        "key": "memory",
        "status": "active",
        "description": (
            "Stores and recalls persistent user information."
        ),
    },

    {
        "name": "Context Engine",
        "key": "context",
        "status": "active",
        "description": (
            "Tracks conversation context and previous messages."
        ),
    },

    {
        "name": "Reasoning Engine",
        "key": "reasoning",
        "status": "active",
        "description": (
            "Performs structured reasoning, comparisons, "
            "and recommendations."
        ),
    },

    {
        "name": "Goal Engine",
        "key": "goal",
        "status": "active",
        "description": (
            "Detects, stores, and manages user goals."
        ),
    },

    {
        "name": "Planner Engine",
        "key": "planner",
        "status": "active",
        "description": (
            "Creates personalized study and learning plans."
        ),
    },

    {
        "name": "Progress Engine",
        "key": "progress",
        "status": "active",
        "description": (
            "Tracks completed topics and learning progress."
        ),
    },
]


# ============================================================
# VALID MODULE STATES
# ============================================================

VALID_STATUSES = {
    "active",
    "offline",
    "error",
    "unknown",
}


# ============================================================
# GET ALL MODULES
# ============================================================

def get_modules():
    """
    Return all registered HOPE modules.

    Returns:
        list: Registered modules.
    """

    return MODULES.copy()


# ============================================================
# GET ACTIVE MODULES
# ============================================================

def get_active_modules():
    """
    Return only active modules.

    Returns:
        list: Active modules.
    """

    return [
        module
        for module in MODULES
        if module["status"] == "active"
    ]


# ============================================================
# GET OFFLINE MODULES
# ============================================================

def get_offline_modules():
    """
    Return modules that are currently offline.

    Returns:
        list: Offline modules.
    """

    return [
        module
        for module in MODULES
        if module["status"] == "offline"
    ]


# ============================================================
# GET ERROR MODULES
# ============================================================

def get_error_modules():
    """
    Return modules that are currently in an error state.

    Returns:
        list: Modules with error status.
    """

    return [
        module
        for module in MODULES
        if module["status"] == "error"
    ]


# ============================================================
# GET UNKNOWN MODULES
# ============================================================

def get_unknown_modules():
    """
    Return modules whose state is unknown.

    Returns:
        list: Modules with unknown status.
    """

    return [
        module
        for module in MODULES
        if module["status"] == "unknown"
    ]


# ============================================================
# GET MODULE COUNT
# ============================================================

def get_module_count():
    """
    Return the total number of registered modules.

    Returns:
        int: Total module count.
    """

    return len(MODULES)


# ============================================================
# GET ACTIVE MODULE COUNT
# ============================================================

def get_active_module_count():
    """
    Return the number of active modules.

    Returns:
        int: Active module count.
    """

    return len(get_active_modules())


# ============================================================
# GET OFFLINE MODULE COUNT
# ============================================================

def get_offline_module_count():
    """
    Return the number of offline modules.

    Returns:
        int: Offline module count.
    """

    return len(get_offline_modules())


# ============================================================
# GET ERROR MODULE COUNT
# ============================================================

def get_error_module_count():
    """
    Return the number of modules in error state.

    Returns:
        int: Error module count.
    """

    return len(get_error_modules())


# ============================================================
# GET UNKNOWN MODULE COUNT
# ============================================================

def get_unknown_module_count():
    """
    Return the number of modules in unknown state.

    Returns:
        int: Unknown module count.
    """

    return len(get_unknown_modules())


# ============================================================
# GET MODULE NAMES
# ============================================================

def get_module_names():
    """
    Return the names of all active modules.

    Returns:
        list: Module names.
    """

    return [
        module["name"]
        for module in get_active_modules()
    ]


# ============================================================
# FIND MODULE
# ============================================================

def get_module(key):
    """
    Find a module using its unique key.

    Parameters:
        key (str): Module key.

    Returns:
        dict or None: Matching module.
    """

    if key is None:
        return None

    key = str(key).lower().strip()

    for module in MODULES:

        if module["key"] == key:
            return module

    return None


# ============================================================
# GET MODULE DESCRIPTION
# ============================================================

def get_module_description(key):
    """
    Return the description of a module.

    Parameters:
        key (str): Module key.

    Returns:
        str or None: Module description.
    """

    module = get_module(key)

    if module is None:
        return None

    return module.get(
        "description",
        "No description available."
    )


# ============================================================
# CHECK MODULE STATUS
# ============================================================

def get_module_status(key):
    """
    Return the current status of a module.

    Parameters:
        key (str): Module key.

    Returns:
        str or None: Module status.
    """

    module = get_module(key)

    if module is None:
        return None

    return module.get(
        "status",
        "unknown"
    )


# ============================================================
# CHECK MODULE ACTIVE
# ============================================================

def is_module_active(key):
    """
    Check whether a module is active.

    Parameters:
        key (str): Module key.

    Returns:
        bool: True if the module is active.
    """

    module = get_module(key)

    if module is None:
        return False

    return module["status"] == "active"


# ============================================================
# CHECK MODULE OFFLINE
# ============================================================

def is_module_offline(key):
    """
    Check whether a module is offline.

    Parameters:
        key (str): Module key.

    Returns:
        bool: True if the module is offline.
    """

    module = get_module(key)

    if module is None:
        return False

    return module["status"] == "offline"


# ============================================================
# CHECK MODULE ERROR
# ============================================================

def is_module_error(key):
    """
    Check whether a module is in an error state.

    Parameters:
        key (str): Module key.

    Returns:
        bool: True if the module has an error.
    """

    module = get_module(key)

    if module is None:
        return False

    return module["status"] == "error"


# ============================================================
# CHECK MODULE UNKNOWN
# ============================================================

def is_module_unknown(key):
    """
    Check whether a module has an unknown state.

    Parameters:
        key (str): Module key.

    Returns:
        bool: True if the module state is unknown.
    """

    module = get_module(key)

    if module is None:
        return False

    return module["status"] == "unknown"


# ============================================================
# SET MODULE STATUS
# ============================================================

def set_module_status(key, status):
    """
    Change the state of a registered module.

    Parameters:
        key (str): Module key.
        status (str): New module status.

    Returns:
        dict or None: Updated module.

    Raises:
        ValueError: If the status is invalid.
    """

    if key is None:
        return None

    if status is None:
        raise ValueError(
            "Module status cannot be None."
        )

    key = str(key).lower().strip()
    status = str(status).lower().strip()

    if status not in VALID_STATUSES:
        raise ValueError(
            f"Invalid module status: '{status}'. "
            f"Valid statuses are: "
            f"{', '.join(sorted(VALID_STATUSES))}"
        )

    module = get_module(key)

    if module is None:
        return None

    module["status"] = status

    return module


# ============================================================
# ENABLE MODULE
# ============================================================

def enable_module(key):
    """
    Set a module to active state.

    Parameters:
        key (str): Module key.

    Returns:
        dict or None: Updated module.
    """

    return set_module_status(
        key,
        "active"
    )


# ============================================================
# DISABLE MODULE
# ============================================================

def disable_module(key):
    """
    Set a module to offline state.

    Parameters:
        key (str): Module key.

    Returns:
        dict or None: Updated module.
    """

    return set_module_status(
        key,
        "offline"
    )


# ============================================================
# SET MODULE ERROR
# ============================================================

def set_module_error(key):
    """
    Set a module to error state.

    Parameters:
        key (str): Module key.

    Returns:
        dict or None: Updated module.
    """

    return set_module_status(
        key,
        "error"
    )


# ============================================================
# SET MODULE UNKNOWN
# ============================================================

def set_module_unknown(key):
    """
    Set a module to unknown state.

    Parameters:
        key (str): Module key.

    Returns:
        dict or None: Updated module.
    """

    return set_module_status(
        key,
        "unknown"
    )


# ============================================================
# RESET ALL MODULES
# ============================================================

def reset_modules():
    """
    Reset all registered modules to active state.

    Returns:
        list: Updated module list.
    """

    for module in MODULES:
        module["status"] = "active"

    return MODULES.copy()