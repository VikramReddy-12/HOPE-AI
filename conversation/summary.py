from conversation.manager import get_conversation


def summarize_conversation():
    """
    Returns a simple summary of the current conversation,
    excluding the current summary request.
    """

    conversation = get_conversation()

    if not conversation:
        return "We haven't talked about anything yet."

    summary = []

    # Skip the last message if it's the user's summary request
    messages = conversation

    if (
        messages
        and messages[-1]["speaker"] == "user"
        and messages[-1]["message"].lower().strip().replace("?", "") in [
            "what did we talk about",
            "summarize our conversation",
            "conversation summary",
            "summarize the conversation",
        ]
    ):
        messages = messages[:-1]

    for message in messages:
        speaker = message["speaker"].capitalize()
        text = message["message"]
        summary.append(f"{speaker}: {text}")

    return "\n".join(summary)