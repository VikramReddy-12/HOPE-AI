from assistant.commands import process_command
from memory.manager import remember, recall
from conversation.manager import get_last_user_message
from conversation.summary import summarize_conversation
from knowledge.engine import search_knowledge
from reasoning.engine import reason


def route(result):
    """
    Route the detected intent to the appropriate module.
    """

    intent = result["intent"]

    print(f"[Router] Intent : {intent}")

    # -----------------------------
    # Greetings
    # -----------------------------
    if intent == "GREETING":
        return process_command(result["command"])

    # -----------------------------
    # Time / Date
    # -----------------------------
    elif intent == "TIME_REQUEST":
        return process_command(result["command"])

    elif intent == "DATE_REQUEST":
        return process_command(result["command"])

    # -----------------------------
    # Help
    # -----------------------------
    elif intent == "HELP":
        return process_command(result["command"])

    # -----------------------------
    # Memory Save
    # -----------------------------
    elif intent == "MEMORY_SAVE":

        if "key" in result and "value" in result:

            key = result["key"]
            value = result["value"]

        else:

            command = result["command"]

            parts = command.split(" ", 2)

            if len(parts) != 3:
                return "Usage: remember <key> <value>"

            key = parts[1]
            value = parts[2]

        print("[Router] Saving Memory")
        print(f"[Router] Key   : {key}")
        print(f"[Router] Value : {value}")

        return remember(key, value)

    # -----------------------------
    # Memory Recall
    # -----------------------------
    elif intent == "MEMORY_RECALL":

        command = result["command"]

        parts = command.split(" ", 1)

        if len(parts) == 2:

            key = parts[1]

            print("[Router] Recalling Memory")
            print(f"[Router] Key : {key}")

            value = recall(key)

            if value:
                return value

            return "I don't remember that."

        return "Usage: recall <key>"

    # -----------------------------
    # Conversation
    # -----------------------------
    elif intent == "LAST_USER_MESSAGE":

        last_message = get_last_user_message(skip_current=True)

        if last_message:
            return f'You said: "{last_message}"'

        return "I don't remember you saying anything yet."

    elif intent == "CONVERSATION_SUMMARY":

        return summarize_conversation()

    # -----------------------------
    # Knowledge Search
    # -----------------------------
    elif intent == "KNOWLEDGE_SEARCH":

        command = result["command"]

        response = reason(command)

        if response is not None:
            return response

        return search_knowledge(command)

    # -----------------------------
    # Comparison
    # -----------------------------
    elif intent == "COMPARE":

        command = result["command"]

        return reason(command)

    # -----------------------------
    # Recommendation
    # -----------------------------
    elif intent == "RECOMMEND":

        command = result["command"]

        return reason(command)

    # -----------------------------
    # Exit
    # -----------------------------
    elif intent == "EXIT":

        return "Goodbye!"

    # -----------------------------
    # Unknown
    # -----------------------------
    else:

        command = result.get("command", "")

        return process_command(command)