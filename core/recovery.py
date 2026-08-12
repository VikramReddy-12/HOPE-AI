"""
HOPE Recovery Engine

Provides automatic recovery capabilities for
unhealthy HOPE modules.

The Recovery Engine works with the central
Module Registry and Diagnostics Engine.
"""

from core.modules import (
    get_module,
    enable_module,
)

from core.diagnostics import (
    check_modules,
    get_health,
)

from core.recovery_log import (
    log_recovery_event,
)


# ============================================================
# RECOVERY RESULT
# ============================================================

def _build_result(
    success,
    module,
    action,
    message,
):
    """
    Build a standardized recovery result.

    Parameters:
        success (bool): Whether recovery succeeded.
        module (dict or None): Module information.
        action (str): Recovery action performed.
        message (str): Recovery message.

    Returns:
        dict: Recovery result.
    """

    return {
        "success": success,
        "module": module,
        "action": action,
        "message": message,
    }


# ============================================================
# CHECK MODULE RECOVERABILITY
# ============================================================

def can_recover(key):
    """
    Determine whether a module can be automatically recovered.

    Parameters:
        key (str): Module key.

    Returns:
        bool: True if the module can be recovered.
    """

    module = get_module(key)

    if module is None:
        return False

    status = module.get(
        "status",
        "unknown"
    ).lower()

    return status in [
        "offline",
        "error",
        "unknown",
    ]


# ============================================================
# RECOVER MODULE
# ============================================================

def recover_module(
    key,
    health_before=None,
):
    """
    Attempt to recover a single unhealthy module.

    Parameters:
        key (str): Module key.
        health_before (str, optional):
            System health before recovery.

    Returns:
        dict: Recovery result.
    """

    module = get_module(key)

    # --------------------------------------------------------
    # Module does not exist
    # --------------------------------------------------------

    if module is None:

        return _build_result(
            False,
            None,
            "none",
            f"Module '{key}' was not found."
        )

    # --------------------------------------------------------
    # Already active
    # --------------------------------------------------------

    status = module.get(
        "status",
        "unknown"
    ).lower()

    if status == "active":

        return _build_result(
            True,
            module,
            "none",
            f"{module['name']} is already active."
        )

    # --------------------------------------------------------
    # Save original failure state
    # --------------------------------------------------------

    failure_status = status.upper()

    # --------------------------------------------------------
    # Check whether recovery is possible
    # --------------------------------------------------------

    if not can_recover(key):

        if health_before is None:
            health_before = get_health()

        health_after = get_health()

        log_recovery_event(
            module=module["name"],
            failure=failure_status,
            action="NONE",
            result="FAILED",
            health_before=health_before,
            health_after=health_after,
        )

        return _build_result(
            False,
            module,
            "none",
            (
                f"{module['name']} cannot be "
                "recovered automatically."
            )
        )

    # --------------------------------------------------------
    # Capture health before recovery
    # --------------------------------------------------------

    if health_before is None:
        health_before = get_health()

    # --------------------------------------------------------
    # Attempt recovery
    # --------------------------------------------------------

    restored = enable_module(key)

    if restored is None:

        health_after = get_health()

        log_recovery_event(
            module=module["name"],
            failure=failure_status,
            action="ENABLE",
            result="FAILED",
            health_before=health_before,
            health_after=health_after,
        )

        return _build_result(
            False,
            module,
            "enable",
            f"Recovery failed for {module['name']}."
        )

    # --------------------------------------------------------
    # Verify recovery
    # --------------------------------------------------------

    verified = get_module(key)

    if verified is None:

        health_after = get_health()

        log_recovery_event(
            module=module["name"],
            failure=failure_status,
            action="ENABLE",
            result="FAILED",
            health_before=health_before,
            health_after=health_after,
        )

        return _build_result(
            False,
            restored,
            "enable",
            f"{module['name']} could not be verified."
        )

    verified_status = verified.get(
        "status",
        "unknown"
    ).lower()

    # --------------------------------------------------------
    # Recovery successful
    # --------------------------------------------------------

    if verified_status == "active":

        health_after = get_health()

        log_recovery_event(
            module=verified["name"],
            failure=failure_status,
            action="ENABLE",
            result="SUCCESS",
            health_before=health_before,
            health_after=health_after,
        )

        return _build_result(
            True,
            verified,
            "enable",
            (
                f"{verified['name']} "
                "recovered successfully."
            )
        )

    # --------------------------------------------------------
    # Recovery verification failed
    # --------------------------------------------------------

    health_after = get_health()

    log_recovery_event(
        module=verified["name"],
        failure=failure_status,
        action="ENABLE",
        result="FAILED",
        health_before=health_before,
        health_after=health_after,
    )

    return _build_result(
        False,
        verified,
        "enable",
        (
            f"{verified['name']} recovery "
            "could not be verified."
        )
    )


# ============================================================
# RECOVER ALL MODULES
# ============================================================

def recover_all():
    """
    Attempt to recover all unhealthy modules.

    Returns:
        list: Recovery results.
    """

    diagnostics = check_modules()

    results = []

    health_before = get_health()

    for module in diagnostics:

        status = module.get(
            "status",
            "unknown"
        ).lower()

        if status != "active":

            result = recover_module(
                module["key"],
                health_before=health_before,
            )

            results.append(result)

            # Update health for subsequent recoveries
            health_before = get_health()

    return results


# ============================================================
# AUTOMATIC RECOVERY
# ============================================================

def automatic_recovery():
    """
    Detect unhealthy modules and automatically
    attempt recovery.

    Returns:
        dict: Complete recovery report.
    """

    # --------------------------------------------------------
    # Health before recovery
    # --------------------------------------------------------

    before_health = get_health()

    # --------------------------------------------------------
    # Detect affected modules
    # --------------------------------------------------------

    diagnostics = check_modules()

    affected_modules = [
        module
        for module in diagnostics
        if module.get(
            "status",
            "unknown"
        ).lower() != "active"
    ]

    # --------------------------------------------------------
    # Nothing to recover
    # --------------------------------------------------------

    if not affected_modules:

        return {
            "success": True,
            "before_health": before_health,
            "after_health": before_health,
            "recovered": [],
            "failed": [],
            "message": (
                "All HOPE modules are already healthy. "
                "No recovery required."
            ),
        }

    # --------------------------------------------------------
    # Recover affected modules
    # --------------------------------------------------------

    results = []

    current_health = before_health

    for module in affected_modules:

        result = recover_module(
            module["key"],
            health_before=current_health,
        )

        results.append(result)

        current_health = get_health()

    # --------------------------------------------------------
    # Separate successful and failed recovery
    # --------------------------------------------------------

    recovered = [
        result
        for result in results
        if result["success"]
    ]

    failed = [
        result
        for result in results
        if not result["success"]
    ]

    # --------------------------------------------------------
    # Verify final health
    # --------------------------------------------------------

    after_health = get_health()

    success = (
        len(failed) == 0
        and after_health == "GOOD"
    )

    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------

    if success:

        message = (
            "✓ All affected HOPE modules "
            "were recovered successfully."
        )

    elif recovered:

        message = (
            "⚠️ Partial recovery completed. "
            "Some modules remain unhealthy."
        )

    else:

        message = (
            "❌ Automatic recovery failed. "
            "Unhealthy modules remain."
        )

    return {
        "success": success,
        "before_health": before_health,
        "after_health": after_health,
        "recovered": recovered,
        "failed": failed,
        "message": message,
    }


# ============================================================
# RECOVERY REPORT
# ============================================================

def get_recovery_report():
    """
    Run automatic recovery and return
    a formatted recovery report.

    Returns:
        str: Recovery report.
    """

    result = automatic_recovery()

    lines = [
        "🔧 HOPE Automatic Recovery",
        "",
        f"Health Before : {result['before_health']}",
        f"Health After  : {result['after_health']}",
        "",
    ]

    # --------------------------------------------------------
    # Recovered modules
    # --------------------------------------------------------

    if result["recovered"]:

        lines.append("✓ Recovered Modules")

        for recovery in result["recovered"]:

            module = recovery["module"]

            lines.append(
                f"  ✓ {module['name']}"
            )

            lines.append(
                f"    {recovery['message']}"
            )

        lines.append("")

    # --------------------------------------------------------
    # Failed modules
    # --------------------------------------------------------

    if result["failed"]:

        lines.append("❌ Failed Recovery")

        for recovery in result["failed"]:

            module = recovery["module"]

            if module is not None:
                name = module["name"]
            else:
                name = "Unknown Module"

            lines.append(
                f"  ✗ {name}"
            )

            lines.append(
                f"    {recovery['message']}"
            )

        lines.append("")

    # --------------------------------------------------------
    # Final message
    # --------------------------------------------------------

    lines.append(
        result["message"]
    )

    return "\n".join(lines)