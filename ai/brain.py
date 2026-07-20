from ai.intent import detect_intent

def think(user_input):

    command = user_input.lower().strip()

    intent = detect_intent(command)

    print(f"[Brain] Input   : {command}")
    print(f"[Brain] Intent : {intent}")

    return command, intent