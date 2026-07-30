"""
HOPE Reference Resolver

This module resolves references such as:
- it
- this
- that
- he
- she
- they

For v1.0, it searches the user's previous
messages from newest to oldest to find
the latest knowledge topic.
"""

from conversation.manager import get_all_user_messages
from knowledge.database import knowledge


def resolve_reference():
    """
    Returns the most recent knowledge topic
    mentioned by the user.

    Returns:
        str | None
    """

    user_messages = get_all_user_messages()

    if not user_messages:
        return None

    # Search from newest to oldest
    for message in reversed(user_messages):

        text = message.lower()

        for topic in knowledge.keys():

            if topic.lower() in text:
                return topic

    return None