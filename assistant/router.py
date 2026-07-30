from assistant.commands import process_command
from memory.manager import remember, recall
from conversation.manager import get_last_user_message
from conversation.summary import summarize_conversation
from knowledge.engine import search_knowledge
from reasoning.engine import reason


def route(result):

    intent = result["intent"]

    print(f"[Router] Intent : {intent}")

    if intent == "GREETING":
        return process_command(result["command"])

    elif intent == "TIME_REQUEST":
        return process_command(result["command"])

    elif intent == "DATE_REQUEST":
        return process_command(result["command"])

    elif intent == "HELP":
        return process_command(result["command"])

    elif intent == "MEMORY_SAVE":

        # Case 1: NLU already extracted key and value
        if "key" in result and "value" in result:

            key = result["key"]
            value = result["value"]

        # Case 2: Old remember command
        else:

            command = result["command"]

            parts = command.split(" ", 2)

            if len(parts) != 3:
                return "Usage: remember <key> <value>"

            key = parts[1]
            value = parts[2]

        print(f"[Router] Saving Memory")
        print(f"[Router] Key   : {key}")
        print(f"[Router] Value : {value}")

        return remember(key, value)

    elif intent == "MEMORY_RECALL":

        command = result["command"]

        parts = command.split(" ", 1)

        if len(parts) == 2:

            key = parts[1]

            print(f"[Router] Recalling Memory")
            print(f"[Router] Key : {key}")

            value = recall(key)

            if value:
                return value

            return "I don't remember that."

        return "Usage: recall <key>"

    elif intent == "LAST_USER_MESSAGE":

        last_message = get_last_user_message(skip_current=True)

        if last_message:
            return f'You said: "{last_message}"'

        return "I don't remember you saying anything yet."

    elif intent == "CONVERSATION_SUMMARY":

        return summarize_conversation()

    elif intent == "KNOWLEDGE_SEARCH":

        command = result["command"]

        # First try the Reasoning Engine
        response = reason(command)

        # If reasoning succeeded, return its response
        if response is not None:
            return response

        # Otherwise, use the Knowledge Engine
        return search_knowledge(command)

    elif intent == "EXIT":

        return "Goodbye!"

    else:

        command = result.get("command", "")

        return process_command(command)