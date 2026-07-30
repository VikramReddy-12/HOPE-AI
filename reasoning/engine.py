"""
HOPE Reasoning Engine

This module combines different HOPE components
to provide intelligent responses.

For v1.0, it uses the Reference Resolver and
Knowledge Engine for follow-up questions.
"""

import string

from reasoning.resolver import resolve_reference
from knowledge.engine import search_knowledge


# Words that indicate the user is referring
# to something mentioned earlier.
REFERENCE_WORDS = [
    "it",
    "this",
    "that",
    "he",
    "she",
    "they"
]


def reason(command):
    """
    Uses reasoning to answer follow-up questions.

    Parameters:
        command (str): User input.

    Returns:
        str | None
    """

    # Preserve the original command
    original_command = command.lower()

    # Create a cleaned version only for detection
    clean_command = original_command.translate(
        str.maketrans("", "", string.punctuation)
    )

    # Check whether reasoning is needed
    needs_reasoning = any(
        word in clean_command.split()
        for word in REFERENCE_WORDS
    )

    if not needs_reasoning:
        return None

    # Resolve the reference
    topic = resolve_reference()

    if topic is None:
        return (
            "I'm not sure what you're referring to. "
            "Could you please be more specific?"
        )

    # Replace only the reference words while
    # preserving the rest of the command.
    words = original_command.split()

    for index, word in enumerate(words):

        cleaned_word = word.strip(string.punctuation)

        if cleaned_word in REFERENCE_WORDS:

            # Preserve punctuation after the word
            suffix = word[len(cleaned_word):]

            words[index] = topic + suffix

    new_command = " ".join(words)

    # Ask the Knowledge Engine
    return search_knowledge(new_command)