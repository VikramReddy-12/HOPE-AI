from assistant.commands import process_command
from memory.manager import remember, recall


def route(command, intent):

    # Debug message
    print(f"[Router] Intent : {intent}")
    print(f"[Router] Command: {command}")

    if intent == "GREETING":
        return process_command(command)

    elif intent == "TIME_REQUEST":
        return process_command(command)

    elif intent == "DATE_REQUEST":
        return process_command(command)

    elif intent == "HELP":
        return process_command(command)

    elif intent == "MEMORY_SAVE":

        parts = command.split(" ", 2)

        if len(parts) == 3:

            key = parts[1]
            value = parts[2]

            print(f"[Router] Saving Memory")
            print(f"[Router] Key   : {key}")
            print(f"[Router] Value : {value}")

            return remember(key, value)

        return "Usage: remember <key> <value>"

    elif intent == "MEMORY_RECALL":

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

    else:

        return process_command(command)