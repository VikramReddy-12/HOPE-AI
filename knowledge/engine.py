"""
HOPE Knowledge Engine

Searches the structured knowledge database
and returns answers based on the user's question.
"""

from knowledge.database import knowledge


# Maps keywords in a question to knowledge fields.
FIELD_MAP = {

    "creator": [
        "who created",
        "creator"
    ],

    "released": [
        "when was",
        "released",
        "release"
    ],

    "uses": [
        "used for",
        "uses",
        "use"
    ],

    # IMPORTANT:
    # Keep "disadvantages" before "advantages"
    # because "advantages" is part of the word
    # "disadvantages".
    "disadvantages": [
        "disadvantages",
        "drawbacks",
        "cons"
    ],

    "advantages": [
        "advantages",
        "benefits",
        "pros"
    ],

    "difficulty": [
        "beginner",
        "difficulty",
        "easy",
        "hard"
    ],

    "best_for": [
        "best for",
        "good for"
    ],

    "definition": [
        "tell me about",
        "what is",
        "explain"
    ]
}


def find_topics(question):
    """
    Find all known topics in a question.

    Parameters:
        question (str)

    Returns:
        list[str]
    """

    question = question.lower().strip()

    topics = []

    for topic in knowledge.keys():

        if topic in question:

            topics.append(topic)

    return topics


def search_knowledge(question):
    """
    Search the structured knowledge database.

    Parameters:
        question (str)

    Returns:
        str
    """

    question = question.lower().strip()

    # ---------------------------------
    # Find all matching topics
    # ---------------------------------

    topics = find_topics(question)

    if not topics:
        return "I don't know that yet."

    # For now, use the first topic.
    # Later (v1.1) the Reasoning Engine
    # will use all detected topics.
    topic_found = topics[0]

    topic_data = knowledge[topic_found]

    # ---------------------------------
    # Determine which field is requested
    # ---------------------------------

    field = "definition"

    keyword_pairs = []

    for key, keywords in FIELD_MAP.items():

        for keyword in keywords:

            keyword_pairs.append((keyword, key))

    # Longest keyword first
    keyword_pairs.sort(
        key=lambda item: len(item[0]),
        reverse=True
    )

    for keyword, key in keyword_pairs:

        if keyword in question:

            field = key
            break

    # ---------------------------------
    # Return the requested information
    # ---------------------------------

    if field not in topic_data:

        return (
            f"I don't have "
            f"{field.replace('_', ' ')} "
            f"information for {topic_found.title()}."
        )

    answer = topic_data[field]

    if isinstance(answer, list):

        return "\n".join(
            f"• {item}"
            for item in answer
        )

    return answer