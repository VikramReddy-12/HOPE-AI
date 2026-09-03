"""
HOPE Version Information

Stores application metadata including
version, release information, author,
repository, loaded modules, and supported features.
"""

# ==========================================================
# Application Information
# ==========================================================

APP_NAME = "HOPE"
FULL_NAME = "Helping Optimize Potential Everyday"

# ==========================================================
# Version Information
# ==========================================================

VERSION = "v1.6"
CODENAME = "Adaptive Intelligence & Accountability"
STATUS = "Stable"

# ==========================================================
# Author Information
# ==========================================================

AUTHOR = "Vikram Reddy"
COPYRIGHT = "© 2026 Vikram Reddy"

# ==========================================================
# Repository
# ==========================================================

REPOSITORY = "https://github.com/VikramReddy-12/HOPE-AI"

# ==========================================================
# Release Information
# ==========================================================

RELEASE_DATE = "September 2026"

DESCRIPTION = (
    "HOPE AI is an intelligent personal assistant "
    "built completely from scratch in Python."
)

# ==========================================================
# Loaded Modules
# ==========================================================

MODULES = [
    "Brain Engine",
    "Knowledge Engine",
    "Memory Engine",
    "Context Engine",
    "Reasoning Engine",
    "Goal Engine",
    "Planner Engine",
    "Progress Engine",
    "Predictive Intelligence Engine",
    "Cross-Engine Intelligence",
    "Decision Synthesis",
    "Response Synthesis",
    "Learning Feedback",
    "Experience Memory",
    "Intelligence Orchestrator",

    # ------------------------------------------------------
    # Adaptive Intelligence Stack
    # ------------------------------------------------------

    "Adaptive Intelligence",
    "Adaptive Strategy",
    "Adaptive Orchestration",
    "Adaptive Decision",
    "Adaptive Response",
    "Adaptive Learning",
    "Adaptive Experience",
    "Adaptive Integration",
    "Adaptive Safety",
    "Adaptive Validation",
    "Adaptive Intelligence Orchestrator",
    "Adaptive Governance",
    "Adaptive Oversight",
    "Adaptive Accountability",
]

# ==========================================================
# Supported Features
# ==========================================================

FEATURES = [
    "Natural Language Understanding",
    "Knowledge Search",
    "Reference Resolution",
    "Topic Comparison",
    "Recommendation Engine",
    "Conversation Memory",
    "Goal Detection",
    "Goal Planning",
    "Progress Tracking",
    "Study Planner",
    "Predictive Intelligence",
    "Decision Safety",
    "Intelligent Pipeline Routing",
    "Shared Orchestration Context",
    "Cross-Engine Intelligence",
    "Decision Synthesis",
    "Intelligent Response Synthesis",
    "Learning Feedback",
    "Experience Memory",

    # ------------------------------------------------------
    # Adaptive Intelligence Features
    # ------------------------------------------------------

    "Adaptive Intelligence",
    "Adaptive Strategy Selection",
    "Adaptive Orchestration",
    "Adaptive Decision Support",
    "Adaptive Response Generation",
    "Adaptive Learning Signals",
    "Adaptive Experience Integration",
    "Adaptive Layer Integration",
    "Adaptive Safety Validation",
    "Adaptive Regression Validation",
    "Adaptive Orchestrator",

    # ------------------------------------------------------
    # Adaptive Governance & Accountability
    # ------------------------------------------------------

    "Adaptive Governance",
    "Adaptive Oversight",
    "Adaptive Accountability",
    "Human Review Enforcement",
    "Audit Availability",
    "Adaptive Safety Assurance",
]

# ==========================================================
# Safety Model
# ==========================================================

SAFETY_LEVEL = "ADVISORY_ONLY"

EXECUTION_ALLOWED = False
AUTOMATIC_ACTION_ALLOWED = False
SELF_MODIFICATION_ALLOWED = False
DECISION_OVERRIDE_ALLOWED = False


def get_version_info():
    """
    Return the complete HOPE version metadata.
    """

    return {
        "app_name": APP_NAME,
        "full_name": FULL_NAME,
        "version": VERSION,
        "codename": CODENAME,
        "status": STATUS,
        "author": AUTHOR,
        "repository": REPOSITORY,
        "release_date": RELEASE_DATE,
        "description": DESCRIPTION,
        "modules": list(MODULES),
        "features": list(FEATURES),
        "safety_level": SAFETY_LEVEL,
        "execution_allowed": EXECUTION_ALLOWED,
        "automatic_action_allowed": AUTOMATIC_ACTION_ALLOWED,
        "self_modification_allowed": SELF_MODIFICATION_ALLOWED,
        "decision_override_allowed": DECISION_OVERRIDE_ALLOWED,
    }


def validate_version_safety():
    """
    Validate the global version safety contract.
    """

    return (
        SAFETY_LEVEL == "ADVISORY_ONLY"
        and EXECUTION_ALLOWED is False
        and AUTOMATIC_ACTION_ALLOWED is False
        and SELF_MODIFICATION_ALLOWED is False
        and DECISION_OVERRIDE_ALLOWED is False
    )