from conversation.context import conversation


def add_message(speaker, message):
    """
    Add a message to the conversation.
    """

    conversation.append({
        "speaker": speaker,
        "message": message
    })


def get_last_message():
    """
    Return the last message.
    """

    if conversation:
        return conversation[-1]

    return None


def get_conversation():
    """
    Return the whole conversation.
    """

    return conversation


def get_all_user_messages():
    """
    Return all user messages in chronological order.

    Returns:
        list[str]
    """

    user_messages = []

    for message in conversation:

        if message["speaker"] == "user":
            user_messages.append(message["message"])

    return user_messages


def get_last_user_message(skip_current=False):
    """
    Return the most recent user message.

    If skip_current=True, return the previous user message
    instead of the current one.
    """

    user_messages = get_all_user_messages()

    if not user_messages:
        return None

    if skip_current:

        if len(user_messages) >= 2:
            return user_messages[-2]

        return None

    return user_messages[-1]


def clear_conversation():
    """
    Clear the conversation.
    """

    conversation.clear()