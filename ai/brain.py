from ai.intent import detect_intent
from ai.nlu import understand


def think(user_input):

    command = user_input.strip()

    # First try normal intent detection
    intent = detect_intent(command)

    # If not understood, ask the NLU
    if intent == "UNKNOWN":

        nlu_result = understand(command)

        if nlu_result:

            print(f"[Brain] Input   : {command}")
            print("[Brain] Intent  : NLU_MATCH")
            print(f"[Brain] NLU     : {nlu_result}")

            return nlu_result

    # Normal processing
    command = command.lower().strip()

    print(f"[Brain] Input   : {command}")
    print(f"[Brain] Intent  : {intent}")

    return {
        "intent": intent,
        "command": command
    }