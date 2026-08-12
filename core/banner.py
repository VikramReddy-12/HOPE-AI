"""
HOPE Banner

Displays the startup banner for HOPE AI.
"""

from core.version import (
    APP_NAME,
    VERSION,
    CODENAME,
    FULL_NAME,
    STATUS,
    AUTHOR,
)

from core.modules import get_active_modules


def show_banner():
    """
    Display the HOPE startup banner.
    """

    print("=" * 60)
    print(f"             {APP_NAME} {VERSION} {CODENAME}")
    print("=" * 60)

    print()
    print("Hello Vikram!")
    print()

    print(f"{APP_NAME} ({FULL_NAME})")
    print()

    print("Your intelligent AI assistant is starting...")
    print()

    print(f"Status : {STATUS.upper()}")
    print()

    # ========================================================
    # DYNAMIC MODULE LIST
    # ========================================================

    print("Loading Modules")
    print("-" * 30)

    modules = get_active_modules()

    for module in modules:
        print(f"✓ {module['name']}")

    # ========================================================
    # SYSTEM READY
    # ========================================================

    print()
    print("System Ready")
    print("-" * 30)

    print("HOPE is ready to talk.")
    print("Type 'help' for available commands.")
    print("Type 'exit' to close HOPE.")

    print()
    print(f"Version : {VERSION}")
    print(f"Release : {CODENAME}")
    print(f"Author  : {AUTHOR}")
    print()