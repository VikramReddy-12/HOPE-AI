"""
HOPE Intent Detection Engine

This module detects the user's intent before the
request is sent to the Router.
"""


def detect_intent(command):
    """
    Detect the user's intent.

    Parameters:
        command (str): User input.

    Returns:
        str: Detected intent.
    """

    command = command.lower().strip()

    # Remove common punctuation
    command = (
        command.replace("?", "")
               .replace(".", "")
               .replace("!", "")
    )

    # -----------------------------
    # Greetings
    # -----------------------------
    if command in [
        "hello",
        "hi",
        "hey"
    ]:
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
    # Comparison
    # -----------------------------
    elif (
        command.startswith("compare ")
        or command.startswith("compare between ")
        or command.startswith("difference between ")
        or command.startswith("difference of ")
        or " vs " in command
        or " versus " in command
        or " compare " in command
        or " or " in command
    ):
        return "COMPARE"

    # -----------------------------
    # Recommendation
    # -----------------------------
    elif (
        command.startswith("should i ")
        or command.startswith("recommend ")
        or command.startswith("which is better")
        or command.startswith("which language")
        or command.startswith("best language")
        or command.startswith("best programming language")
        or command.startswith("what should i learn")
        or command.startswith("which should i choose")
        or command.startswith("which one is better")
    ):
        return "RECOMMEND"

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
        or command.startswith("advantages of ")
        or command.startswith("disadvantages of ")
        or command.startswith("pros of ")
        or command.startswith("cons of ")
        or command.startswith("benefits of ")
        or command.startswith("drawbacks of ")
        or command.startswith("uses of ")
        or command.startswith("purpose of ")
        or command.startswith("best for ")
        or command.startswith("is ")
        or "used for" in command
        or "advantages" in command
        or "disadvantages" in command
        or "benefits" in command
        or "pros" in command
        or "cons" in command
        or "best for" in command
        or "beginner" in command
        or "easy" in command
        or "hard" in command
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