"""
HOPE Diagnostics Engine

Provides system and module diagnostic information
using the central HOPE Module Registry.

Failure Detection Layer:

    ACTIVE   -> OK
    OFFLINE  -> OFFLINE
    ERROR    -> ERROR
    UNKNOWN  -> UNKNOWN
"""

from core.modules import (
    get_modules,
)


# ============================================================
# HEALTH LEVELS
# ============================================================

GOOD = "GOOD"
WARNING = "WARNING"
DEGRADED = "DEGRADED"
CRITICAL = "CRITICAL"


# ============================================================
# MODULE DIAGNOSTICS
# ============================================================

def check_modules():
    """
    Check all registered HOPE modules.

    Returns:
        list: Diagnostic information for each module.
    """

    modules = get_modules()

    diagnostics = []

    for module in modules:

        name = module.get(
            "name",
            "Unknown Module"
        )

        key = module.get(
            "key",
            "unknown"
        )

        status = str(
            module.get(
                "status",
                "unknown"
            )
        ).lower().strip()

        # ----------------------------------------------------
        # ACTIVE
        # ----------------------------------------------------

        if status == "active":

            health = "OK"
            error = None

        # ----------------------------------------------------
        # OFFLINE
        # ----------------------------------------------------

        elif status in [
            "offline",
            "inactive",
            "disabled",
        ]:

            health = "OFFLINE"
            error = None

        # ----------------------------------------------------
        # ERROR
        # ----------------------------------------------------

        elif status in [
            "error",
            "failed",
            "failure",
        ]:

            health = "ERROR"

            error = module.get(
                "error",
                "Module reported an error."
            )

        # ----------------------------------------------------
        # UNKNOWN
        # ----------------------------------------------------

        else:

            health = "UNKNOWN"

            error = module.get(
                "error",
                "Unknown module status."
            )

        diagnostics.append({
            "name": name,
            "key": key,
            "status": status,
            "health": health,
            "error": error,
        })

    return diagnostics


# ============================================================
# OFFLINE MODULES
# ============================================================

def get_offline_modules():
    """
    Return modules that are offline.

    Returns:
        list: Offline modules.
    """

    diagnostics = check_modules()

    return [
        module
        for module in diagnostics
        if module["health"] == "OFFLINE"
    ]


# ============================================================
# MODULE ERRORS
# ============================================================

def get_module_errors():
    """
    Return modules that have errors.

    Returns:
        list: Modules with errors.
    """

    diagnostics = check_modules()

    return [
        module
        for module in diagnostics
        if module["health"] == "ERROR"
    ]


# ============================================================
# UNKNOWN MODULES
# ============================================================

def get_unknown_modules():
    """
    Return modules with unknown status.

    Returns:
        list: Unknown modules.
    """

    diagnostics = check_modules()

    return [
        module
        for module in diagnostics
        if module["health"] == "UNKNOWN"
    ]


# ============================================================
# UNHEALTHY MODULES
# ============================================================

def get_unhealthy_modules():
    """
    Return all modules that are not healthy.

    Includes:

        OFFLINE
        ERROR
        UNKNOWN

    Returns:
        list: Unhealthy modules.
    """

    diagnostics = check_modules()

    return [
        module
        for module in diagnostics
        if module["health"] != "OK"
    ]


# ============================================================
# HEALTH SUMMARY
# ============================================================

def get_health_summary():
    """
    Return structured HOPE health information.

    Returns:
        dict: Health summary.
    """

    diagnostics = check_modules()

    total = len(diagnostics)

    active = sum(
        1
        for module in diagnostics
        if module["health"] == "OK"
    )

    offline = sum(
        1
        for module in diagnostics
        if module["health"] == "OFFLINE"
    )

    errors = sum(
        1
        for module in diagnostics
        if module["health"] == "ERROR"
    )

    unknown = sum(
        1
        for module in diagnostics
        if module["health"] == "UNKNOWN"
    )

    unhealthy = (
        offline
        + errors
        + unknown
    )

    health = get_health()

    return {
        "health": health,
        "total": total,
        "active": active,
        "offline": offline,
        "errors": errors,
        "unknown": unknown,
        "unhealthy": unhealthy,
    }


# ============================================================
# SYSTEM HEALTH
# ============================================================

def get_health():
    """
    Determine overall HOPE system health.

    Health levels:

        GOOD
        WARNING
        DEGRADED
        CRITICAL

    Returns:
        str: Overall system health.
    """

    diagnostics = check_modules()

    total = len(diagnostics)

    # --------------------------------------------------------
    # No modules
    # --------------------------------------------------------

    if total == 0:
        return CRITICAL

    # --------------------------------------------------------
    # Count module states
    # --------------------------------------------------------

    active = sum(
        1
        for module in diagnostics
        if module["health"] == "OK"
    )

    offline = sum(
        1
        for module in diagnostics
        if module["health"] == "OFFLINE"
    )

    errors = sum(
        1
        for module in diagnostics
        if module["health"] == "ERROR"
    )

    unknown = sum(
        1
        for module in diagnostics
        if module["health"] == "UNKNOWN"
    )

    unhealthy = (
        offline
        + errors
        + unknown
    )

    # --------------------------------------------------------
    # CRITICAL
    # --------------------------------------------------------

    if active == 0:
        return CRITICAL

    if unknown > 0:
        return CRITICAL

    # --------------------------------------------------------
    # GOOD
    # --------------------------------------------------------

    if active == total:
        return GOOD

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    if unhealthy == 1:
        return WARNING

    # --------------------------------------------------------
    # DEGRADED
    # --------------------------------------------------------

    if active > 0 and unhealthy > 1:
        return DEGRADED

    return CRITICAL


# ============================================================
# HEALTH MESSAGE
# ============================================================

def get_health_message():
    """
    Return a human-readable health message.

    Returns:
        str: Health explanation.
    """

    health = get_health()

    if health == GOOD:

        return (
            "✓ All registered HOPE modules "
            "are operating normally."
        )

    elif health == WARNING:

        return (
            "⚠️ One HOPE module requires attention."
        )

    elif health == DEGRADED:

        return (
            "⚠️ Multiple HOPE modules require "
            "attention, but the system can "
            "continue operating."
        )

    else:

        return (
            "❌ HOPE has a critical system "
            "condition and may not operate normally."
        )


# ============================================================
# HEALTH RECOMMENDATION
# ============================================================

def get_health_recommendation():
    """
    Return a recommendation based on system health.

    Returns:
        str: Recommended action.
    """

    health = get_health()

    offline = get_offline_modules()
    errors = get_module_errors()
    unknown = get_unknown_modules()

    # --------------------------------------------------------
    # GOOD
    # --------------------------------------------------------

    if health == GOOD:

        return (
            "No action required. "
            "HOPE is operating normally."
        )

    # --------------------------------------------------------
    # WARNING
    # --------------------------------------------------------

    if health == WARNING:

        if offline:

            names = ", ".join(
                module["name"]
                for module in offline
            )

            return (
                f"Restore the offline module: "
                f"{names}."
            )

        if errors:

            names = ", ".join(
                module["name"]
                for module in errors
            )

            return (
                f"Investigate the module error: "
                f"{names}."
            )

        return (
            "Inspect the affected module "
            "before continuing."
        )

    # --------------------------------------------------------
    # DEGRADED
    # --------------------------------------------------------

    if health == DEGRADED:

        affected = (
            offline
            + errors
            + unknown
        )

        names = ", ".join(
            module["name"]
            for module in affected
        )

        return (
            "Multiple modules require attention. "
            f"Affected modules: {names}."
        )

    # --------------------------------------------------------
    # CRITICAL
    # --------------------------------------------------------

    if health == CRITICAL:

        return (
            "Immediately investigate the HOPE "
            "core system and affected modules."
        )

    return "No recommendation available."


# ============================================================
# SYSTEM HEALTH CHECK
# ============================================================

def is_system_healthy():
    """
    Determine whether HOPE is fully healthy.

    Returns:
        bool: True when health is GOOD.
    """

    return get_health() == GOOD


# ============================================================
# HEALTH ICON
# ============================================================

def get_health_icon():
    """
    Return an icon representing system health.

    Returns:
        str: Health icon.
    """

    health = get_health()

    if health == GOOD:
        return "🟢"

    elif health == WARNING:
        return "🟡"

    elif health == DEGRADED:
        return "🟠"

    return "🔴"


# ============================================================
# HEALTH INTELLIGENCE REPORT
# ============================================================

def get_health_report():
    """
    Generate a human-readable Health Intelligence report.

    Returns:
        str: Health analysis report.
    """

    summary = get_health_summary()

    health = summary["health"]

    icon = get_health_icon()

    lines = [
        f"{icon} HOPE Health Intelligence",
        "",
        f"System Health: {health}",
        "",
        f"Modules Checked : {summary['total']}",
        f"Active          : {summary['active']}",
        f"Offline         : {summary['offline']}",
        f"Errors          : {summary['errors']}",
        f"Unknown         : {summary['unknown']}",
        "",
        get_health_message(),
    ]

    # --------------------------------------------------------
    # Affected Modules
    # --------------------------------------------------------

    unhealthy = get_unhealthy_modules()

    if unhealthy:

        lines.extend([
            "",
            "⚠️ Affected Modules:",
        ])

        for module in unhealthy:

            lines.append(
                f"  • {module['name']} "
                f"[{module['health']}]"
            )

            if module["error"]:

                lines.append(
                    f"    Error: {module['error']}"
                )

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    lines.extend([
        "",
        "💡 Recommendation:",
        f"  {get_health_recommendation()}",
    ])

    return "\n".join(lines)


# ============================================================
# SYSTEM DIAGNOSTICS
# ============================================================

def run_diagnostics():
    """
    Run complete HOPE system diagnostics.

    Returns:
        str: Formatted diagnostic report.
    """

    summary = get_health_summary()

    system_health = summary["health"]

    icon = get_health_icon()

    lines = [
        f"{icon} HOPE Diagnostics",
        "",
        f"Modules Checked : {summary['total']}",
        f"Active          : {summary['active']}",
        f"Offline         : {summary['offline']}",
        f"Errors          : {summary['errors']}",
        f"Unknown         : {summary['unknown']}",
        "",
    ]

    # --------------------------------------------------------
    # Module Checks
    # --------------------------------------------------------

    diagnostics = check_modules()

    for module in diagnostics:

        module_health = module["health"]

        if module_health == "OK":
            module_icon = "✓"

        elif module_health == "OFFLINE":
            module_icon = "✗"

        elif module_health == "ERROR":
            module_icon = "!"

        else:
            module_icon = "?"

        lines.append(
            f"{module_icon} "
            f"{module['name']:<20} "
            f"{module_health}"
        )

        if module["error"]:

            lines.append(
                f"    Error: {module['error']}"
            )

    # --------------------------------------------------------
    # Final Health Information
    # --------------------------------------------------------

    lines.extend([
        "",
        f"System Health: {system_health}",
        "",
        get_health_message(),
        "",
        "💡 Recommendation:",
        f"  {get_health_recommendation()}",
    ])

    return "\n".join(lines)