def detect_intent(command):

    command = command.lower().strip()

    # Remove punctuation that users commonly type
    command = command.replace("?", "").replace(".", "").replace("!", "")

    if command in ["hello", "hi", "hey"]:
        return "GREETING"

    elif "time" in command:
        return "TIME_REQUEST"

    elif "date" in command:
        return "DATE_REQUEST"

    elif "help" in command:
        return "HELP"

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

    elif command.startswith("remember "):
        return "MEMORY_SAVE"

    elif command.startswith("recall "):
        return "MEMORY_RECALL"

    # Knowledge Engine (v0.9)
    elif command.startswith("what is "):
        return "KNOWLEDGE_SEARCH"

    elif command.startswith("who is "):
        return "KNOWLEDGE_SEARCH"

    elif command.startswith("who created "):
        return "KNOWLEDGE_SEARCH"

    elif command.startswith("what are "):
        return "KNOWLEDGE_SEARCH"

    elif command.startswith("tell me about "):
        return "KNOWLEDGE_SEARCH"

    elif command.startswith("explain "):
        return "KNOWLEDGE_SEARCH"

    elif command == "exit":
        return "EXIT"

    else:
        return "UNKNOWN"