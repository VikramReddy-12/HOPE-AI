"""
HOPE Reasoning Engine

Provides advanced reasoning capabilities including:

- Reference Resolution
- Topic Comparison
- Recommendations
- Knowledge Reasoning
"""

import string

from reasoning.resolver import resolve_reference
from knowledge.engine import (
    search_knowledge,
    find_topics
)
from knowledge.database import knowledge


# Words indicating that the user is referring
# to something mentioned previously.
REFERENCE_WORDS = [
    "it",
    "this",
    "that",
    "he",
    "she",
    "they"
]


def compare_topics(topics):
    """
    Compare two knowledge topics.
    """

    if len(topics) < 2:
        return None

    topic1 = topics[0]
    topic2 = topics[1]

    data1 = knowledge.get(topic1)
    data2 = knowledge.get(topic2)

    if data1 is None or data2 is None:
        return None

    response = []

    response.append("=" * 60)
    response.append(f"{topic1.title()} vs {topic2.title()}")
    response.append("=" * 60)
    response.append("")

    # ---------------------------------
    # Basic Information
    # ---------------------------------

    fields = [
        ("creator", "Creator"),
        ("released", "Released"),
        ("difficulty", "Difficulty"),
        ("uses", "Uses")
    ]

    for key, title in fields:

        response.append(title)

        response.append(
            f"{topic1.title():<10}: {data1.get(key, 'Unknown')}"
        )

        response.append(
            f"{topic2.title():<10}: {data2.get(key, 'Unknown')}"
        )

        response.append("")

    # ---------------------------------
    # Advantages
    # ---------------------------------

    response.append("Advantages")

    response.append(f"{topic1.title()}:")

    for item in data1.get("advantages", []):
        response.append(f"  ✓ {item}")

    response.append("")

    response.append(f"{topic2.title()}:")

    for item in data2.get("advantages", []):
        response.append(f"  ✓ {item}")

    response.append("")

    # ---------------------------------
    # Disadvantages
    # ---------------------------------

    response.append("Disadvantages")

    response.append(f"{topic1.title()}:")

    for item in data1.get("disadvantages", []):
        response.append(f"  ✗ {item}")

    response.append("")

    response.append(f"{topic2.title()}:")

    for item in data2.get("disadvantages", []):
        response.append(f"  ✗ {item}")

    response.append("")

    # ---------------------------------
    # Best For
    # ---------------------------------

    response.append("Best For")

    response.append(f"{topic1.title()}:")

    for item in data1.get("best_for", []):
        response.append(f"  • {item}")

    response.append("")

    response.append(f"{topic2.title()}:")

    for item in data2.get("best_for", []):
        response.append(f"  • {item}")

    return "\n".join(response)


def recommend(topic):
    """
    Recommend a topic based on its knowledge.
    """

    if topic not in knowledge:
        return None

    data = knowledge[topic]

    response = []

    response.append(f"I recommend learning {topic.title()}.")
    response.append("")

    response.append(
        f"Difficulty : {data.get('difficulty', 'Unknown')}"
    )

    response.append("")

    response.append("Best For:")

    for item in data.get("best_for", []):
        response.append(f"• {item}")

    response.append("")
    response.append("Advantages:")

    for item in data.get("advantages", []):
        response.append(f"✓ {item}")

    return "\n".join(response)


def resolve_references(command):
    """
    Resolve follow-up references such as:
    it, this, that...
    """

    original_command = command.lower()

    clean_command = original_command.translate(
        str.maketrans("", "", string.punctuation)
    )

    needs_reasoning = any(
        word in clean_command.split()
        for word in REFERENCE_WORDS
    )

    if not needs_reasoning:
        return None

    topic = resolve_reference()

    if topic is None:
        return (
            "I'm not sure what you're referring to. "
            "Could you please be more specific?"
        )

    words = original_command.split()

    for index, word in enumerate(words):

        cleaned_word = word.strip(string.punctuation)

        if cleaned_word in REFERENCE_WORDS:

            suffix = word[len(cleaned_word):]

            words[index] = topic + suffix

    return " ".join(words)


def reason(command):
    """
    Main reasoning function.
    """

    command = command.lower().strip()

    # ---------------------------------
    # Detect Topics
    # ---------------------------------

    topics = find_topics(command)

    # ---------------------------------
    # Comparison
    # ---------------------------------

    if (
        (
            "compare" in command
            or "difference" in command
            or " vs " in command
            or " versus " in command
            or " or " in command
        )
        and len(topics) >= 2
    ):

        return compare_topics(topics)

    # ---------------------------------
    # Recommendation
    # ---------------------------------

    if (
        "should i" in command
        or "recommend" in command
        or "better" in command
        or "best language" in command
    ):

        if topics:
            return recommend(topics[0])

    # ---------------------------------
    # Reference Resolution
    # ---------------------------------

    resolved_command = resolve_references(command)

    if resolved_command is not None:
        return search_knowledge(resolved_command)

    # ---------------------------------
    # No reasoning required
    # ---------------------------------

    return None