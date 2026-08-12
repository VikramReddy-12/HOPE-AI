"""
HOPE System Information Engine

Provides dynamic system information about HOPE AI.

This module combines application metadata from version.py,
runtime module information from modules.py, and health
information from the Diagnostics Engine.
"""

from core.version import (
    APP_NAME,
    VERSION,
    CODENAME,
    FULL_NAME,
    STATUS,
    AUTHOR,
    COPYRIGHT,
)

from core.modules import (
    get_modules,
    get_active_modules,
    get_module_count,
    get_active_module_count,
)

from core.diagnostics import (
    get_health,
    get_module_errors,
)


# ============================================================
# ABOUT HOPE
# ============================================================

def get_about():
    """
    Return complete information about HOPE AI.

    Returns:
        str: Formatted HOPE system information.
    """

    modules = get_active_modules()
    module_count = get_active_module_count()

    lines = [
        f"🤖 {APP_NAME}",
        "",
        FULL_NAME,
        "",
        f"Version : {VERSION}",
        f"Codename: {CODENAME}",
        f"Status  : {STATUS}",
        f"Author  : {AUTHOR}",
        "",
        "An intelligent AI assistant built completely "
        "from scratch in Python.",
        "",
        f"🧩 Active Modules: {module_count}",
        "",
    ]

    for module in modules:

        module_status = module["status"].upper()

        lines.append(
            f"✓ {module['name']} [{module_status}]"
        )

        description = module.get(
            "description",
            "No description available."
        )

        lines.append(
            f"  {description}"
        )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# VERSION INFORMATION
# ============================================================

def get_system_version():
    """
    Return HOPE version information.

    Returns:
        str: Version information.
    """

    return (
        f"🤖 {APP_NAME} {VERSION}\n"
        f"Codename: {CODENAME}\n"
        f"Status  : {STATUS}"
    )


# ============================================================
# COPYRIGHT INFORMATION
# ============================================================

def get_system_copyright():
    """
    Return HOPE copyright information.

    Returns:
        str: Copyright information.
    """

    return COPYRIGHT


# ============================================================
# MODULE INFORMATION
# ============================================================

def get_system_modules():
    """
    Return information about all registered HOPE modules.

    Returns:
        str: Formatted module information.
    """

    modules = get_modules()

    lines = [
        f"🧩 HOPE Modules ({len(modules)})",
        "",
    ]

    if not modules:

        lines.append("No modules registered.")

        return "\n".join(lines)

    for module in modules:

        module_status = module["status"].upper()

        if module_status == "ACTIVE":
            icon = "✓"
        else:
            icon = "✗"

        lines.append(
            f"{icon} {module['name']} [{module_status}]"
        )

        description = module.get(
            "description",
            "No description available."
        )

        lines.append(
            f"  {description}"
        )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# ACTIVE MODULE INFORMATION
# ============================================================

def get_active_system_modules():
    """
    Return information about active HOPE modules only.

    Returns:
        str: Formatted active module information.
    """

    modules = get_active_modules()
    active_count = get_active_module_count()

    lines = [
        f"🧩 HOPE Active Modules ({active_count})",
        "",
    ]

    if not modules:

        lines.append("No active modules.")

        return "\n".join(lines)

    for module in modules:

        module_status = module["status"].upper()

        lines.append(
            f"✓ {module['name']} [{module_status}]"
        )

        description = module.get(
            "description",
            "No description available."
        )

        lines.append(
            f"  {description}"
        )

        lines.append("")

    return "\n".join(lines)


# ============================================================
# SYSTEM STATUS
# ============================================================

def get_system_status():
    """
    Return the current HOPE system status.

    Uses the Diagnostics Engine to determine
    overall system health.

    Returns:
        str: Formatted system status.
    """

    modules = get_modules()

    total_modules = get_module_count()
    active_modules = get_active_module_count()

    offline_modules = total_modules - active_modules

    # --------------------------------------------------------
    # Diagnostics Engine
    # --------------------------------------------------------

    health = get_health()
    errors = get_module_errors()

    # --------------------------------------------------------
    # Determine overall system status
    # --------------------------------------------------------

    if total_modules == 0:

        system_status = "OFFLINE"

    elif active_modules == total_modules:

        system_status = "ONLINE"

    elif active_modules > 0:

        system_status = "DEGRADED"

    else:

        system_status = "OFFLINE"

    # --------------------------------------------------------
    # Determine status icon
    # --------------------------------------------------------

    if health == "GOOD":

        status_icon = "🟢"

    elif health == "WARNING":

        status_icon = "🟡"

    else:

        status_icon = "🔴"

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    lines = [
        f"{status_icon} HOPE System Status",
        "",
        f"Version : {VERSION}",
        f"Codename: {CODENAME}",
        f"Status  : {system_status}",
        "",
        f"Modules : {total_modules}",
        f"Active  : {active_modules}",
        f"Offline : {offline_modules}",
        "",
    ]

    # --------------------------------------------------------
    # Module Status
    # --------------------------------------------------------

    if not modules:

        lines.append("No modules registered.")

    else:

        for module in modules:

            module_status = module["status"].upper()

            if module_status == "ACTIVE":

                icon = "✓"

            else:

                icon = "✗"

            lines.append(
                f"{icon} {module['name']} [{module_status}]"
            )

    # --------------------------------------------------------
    # Health
    # --------------------------------------------------------

    lines.extend([
        "",
        f"System Health: {health}",
        f"Diagnostic Errors: {len(errors)}",
    ])

    return "\n".join(lines)