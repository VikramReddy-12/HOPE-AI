"""
HOPE Knowledge Engine

This module searches the built-in knowledge
database and returns the most relevant answer.
"""

from knowledge.database import knowledge


def search_knowledge(question):
    """
    Searches the knowledge database for a matching topic.
    """

    question = question.lower()

    for topic, info in knowledge.items():

        if topic not in question:
            continue

        # Creator
        if (
            "who created" in question
            or "creator" in question
            or "inventor" in question
            or "who invented" in question
        ):
            return info.get("creator", "I don't know that yet.")

        # Release Year
        elif (
            "when was" in question
            or "when did" in question
            or "released" in question
            or "release" in question
        ):
            return info.get("released", "I don't know that yet.")

        # Uses
        elif (
            "used for" in question
            or "uses" in question
            or "use" in question
            or "purpose" in question
            or "application" in question
        ):
            return info.get("uses", "I don't know that yet.")

        # Definition
        elif (
            "what is" in question
            or "tell me about" in question
            or "explain" in question
        ):
            return info.get("definition", "I don't know that yet.")

        # Default
        return info.get("definition", "I don't know that yet.")

    return "I don't know that yet."