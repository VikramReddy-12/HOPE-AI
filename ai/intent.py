"""
HOPE Intent Detection Engine

This module detects the user's intent before the
request is sent to the Router.
"""


def detect_intent(command):

    command = command.lower().strip()

    # Remove common punctuation
    command = command.replace("?", "").replace(".", "").replace("!", "")

    # -----------------------------
    # Greetings
    # -----------------------------
    if command in ["hello", "hi", "hey"]:
        return "GREETING"

    # -----------------------------
    # Time / Date
    # -----------------------------
    elif "time" in command:
        return "TIME_REQUEST"

    elif "date" in command:
        return "DATE_REQUEST"

    # -----------------------------
    # Help
    # -----------------------------
    elif "help" in command:
        return "HELP"

    # -----------------------------
    # Conversation
    # -----------------------------
    elif command in [
        "what did i just say",
        "what was my last message",
        "repeat my last message"
    ]:
        return "LAST_USER_MESSAGE"

    elif command in [
        "what did we talk about",
        "summarize our conversation",
        "conversation summary",
        "summarize the conversation"
    ]:
        return "CONVERSATION_SUMMARY"

    # -----------------------------
    # Memory
    # -----------------------------
    elif command.startswith("remember "):
        return "MEMORY_SAVE"

    elif command.startswith("recall "):
        return "MEMORY_RECALL"

    # -----------------------------
    # Knowledge Search
    # -----------------------------
    elif (
        command.startswith("what is ")
        or command.startswith("what are ")
        or command.startswith("who is ")
        or command.startswith("who created ")
        or command.startswith("who invented ")
        or command.startswith("tell me about ")
        or command.startswith("explain ")
        or command.startswith("when was ")
        or command.startswith("when did ")
        or "used for" in command
        or command.startswith("uses of ")
        or command.startswith("purpose of ")
    ):
        return "KNOWLEDGE_SEARCH"

    # -----------------------------
    # Exit
    # -----------------------------
    elif command == "exit":
        return "EXIT"

    # -----------------------------
    # Unknown
    # -----------------------------
    else:
        return "UNKNOWN"