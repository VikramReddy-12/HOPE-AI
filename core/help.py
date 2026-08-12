"""
HOPE Help Engine

Provides structured help information for HOPE AI.

Supports:
- Full help
- Category-specific help
- Help category aliases
- Dynamic module information
- Unknown category handling
"""

from core.modules import get_active_modules


# ============================================================
# HELP CATEGORIES
# ============================================================

HELP_CATEGORIES = {

    # --------------------------------------------------------
    # Knowledge
    # --------------------------------------------------------

    "knowledge": {
        "title": "📚 Knowledge",
        "commands": [
            ("what is <topic>", "Learn about a topic"),
            ("what are <topic>", "Learn about multiple concepts"),
            ("who is <person>", "Learn about a person"),
            ("tell me about <topic>", "Get information about a topic"),
            ("explain <topic>", "Get an explanation"),
            ("advantages of <topic>", "Learn the advantages"),
            ("disadvantages of <topic>", "Learn the disadvantages"),
            ("uses of <topic>", "Learn common uses"),
        ]
    },

    # --------------------------------------------------------
    # Comparison
    # --------------------------------------------------------

    "comparison": {
        "title": "⚖️ Comparison",
        "commands": [
            ("compare <A> and <B>", "Compare two topics"),
            ("<A> vs <B>", "Compare two topics"),
            ("difference between <A> and <B>", "Find key differences"),
        ]
    },

    # --------------------------------------------------------
    # Recommendation
    # --------------------------------------------------------

    "recommendation": {
        "title": "💡 Recommendations",
        "commands": [
            ("should I <action>", "Get a recommendation"),
            ("recommend <topic>", "Get a recommendation"),
            ("which is better", "Compare choices"),
            ("what should I learn", "Get a learning recommendation"),
        ]
    },

    # --------------------------------------------------------
    # Memory
    # --------------------------------------------------------

    "memory": {
        "title": "🧠 Memory",
        "commands": [
            ("remember <key> <value>", "Save information"),
            ("recall <key>", "Recall saved information"),
        ]
    },

    # --------------------------------------------------------
    # Goals
    # --------------------------------------------------------

    "goals": {
        "title": "🎯 Goals",
        "commands": [
            ("I want to become <goal>", "Set a goal"),
            ("my goal is <goal>", "Set a goal"),
            ("what is my goal", "Recall your current goal"),
        ]
    },

    # --------------------------------------------------------
    # Study & Progress
    # --------------------------------------------------------

    "study": {
        "title": "📚 Study & Progress",
        "commands": [
            (
                "what should I study today",
                "Get today's study plan"
            ),
            (
                "study plan",
                "Show your study plan"
            ),
            (
                "show my progress",
                "View learning progress"
            ),
            (
                "mark <topic> completed",
                "Mark a topic as completed"
            ),
            (
                "what is my next topic",
                "Get the next learning topic"
            ),
        ]
    },

    # --------------------------------------------------------
    # Conversation
    # --------------------------------------------------------

    "conversation": {
        "title": "💬 Conversation",
        "commands": [
            (
                "what did I just say",
                "Recall your last message"
            ),
            (
                "repeat my last message",
                "Repeat your last message"
            ),
            (
                "summarize our conversation",
                "Summarize the conversation"
            ),
        ]
    },

    # --------------------------------------------------------
    # System
    # --------------------------------------------------------

    "system": {
        "title": "⚙️ System",
        "commands": [
            ("about", "Show information about HOPE"),
            ("version", "Show the current version"),
            ("copyright", "Show copyright information"),
            ("status", "Show current HOPE system status"),
            ("help", "Show available commands"),
            ("time", "Show the current time"),
            ("date", "Show the current date"),
            ("exit", "Exit HOPE"),
        ]
    },
}


# ============================================================
# CATEGORY ALIASES
# ============================================================

CATEGORY_ALIASES = {

    # Knowledge
    "knowledge": "knowledge",
    "learn": "knowledge",

    # Comparison
    "comparison": "comparison",
    "compare": "comparison",

    # Recommendation
    "recommendation": "recommendation",
    "recommendations": "recommendation",
    "recommend": "recommendation",

    # Memory
    "memory": "memory",
    "memories": "memory",

    # Goals
    "goal": "goals",
    "goals": "goals",
    "target": "goals",

    # Study
    "study": "study",
    "learning": "study",
    "progress": "study",

    # Conversation
    "conversation": "conversation",
    "chat": "conversation",

    # System
    "system": "system",
    "commands": "system",
}


# ============================================================
# FORMAT CATEGORY
# ============================================================

def _format_category(category):
    """
    Format one help category.

    Parameters:
        category (str): Category key.

    Returns:
        str: Formatted help category.
    """

    data = HELP_CATEGORIES[category]

    lines = [
        data["title"],
        ""
    ]

    for command, description in data["commands"]:
        lines.append(
            f"  {command:<32} {description}"
        )

    return "\n".join(lines)


# ============================================================
# FORMAT MODULES
# ============================================================

def _format_modules():
    """
    Format the active HOPE modules dynamically.

    Returns:
        str: Formatted module list.
    """

    modules = get_active_modules()

    lines = [
        "🧩 Active Modules",
        ""
    ]

    if not modules:
        lines.append("  No active modules.")

        return "\n".join(lines)

    for module in modules:
        lines.append(
            f"  ✓ {module['name']}"
        )

    return "\n".join(lines)


# ============================================================
# FULL HELP
# ============================================================

def get_help():
    """
    Return the complete HOPE help menu.

    Returns:
        str: Complete formatted help.
    """

    lines = [
        "",
        "╔════════════════════════════════════════════════════════════╗",
        "║                     🤖 HOPE HELP                          ║",
        "╚════════════════════════════════════════════════════════════╝",
        ""
    ]

    # --------------------------------------------------------
    # Help Categories
    # --------------------------------------------------------

    for category in HELP_CATEGORIES:

        lines.append(
            _format_category(category)
        )

        lines.append("")

    # --------------------------------------------------------
    # Dynamic Modules
    # --------------------------------------------------------

    lines.append(
        _format_modules()
    )

    lines.extend([
        "",
        "💡 Tip:",
        "  Type 'help <category>' for detailed help.",
        "",
        "Available categories:",
        "  knowledge",
        "  comparison",
        "  recommendation",
        "  memory",
        "  goals",
        "  study",
        "  conversation",
        "  system",
    ])

    return "\n".join(lines)


# ============================================================
# CATEGORY HELP
# ============================================================

def get_category_help(category):
    """
    Return help for a specific category.

    Parameters:
        category (str): Requested category.

    Returns:
        str: Category-specific help.
    """

    if category is None:
        return get_help()

    category = category.lower().strip()

    category = CATEGORY_ALIASES.get(
        category,
        category
    )

    if category not in HELP_CATEGORIES:

        available = ", ".join(
            HELP_CATEGORIES.keys()
        )

        return (
            f"❌ I don't have a help category "
            f"called '{category}'.\n\n"
            f"Available categories:\n"
            f"  {available}"
        )

    return (
        "\n"
        + _format_category(category)
        + "\n"
    )


# ============================================================
# MAIN HELP FUNCTION
# ============================================================

def show_help(category=None):
    """
    Main public interface for the Help Engine.

    Parameters:
        category (str, optional):
            Specific help category.

    Returns:
        str: Formatted help information.
    """

    if category is None:
        return get_help()

    return get_category_help(category)