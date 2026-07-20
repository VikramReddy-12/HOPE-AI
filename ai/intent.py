def detect_intent(command):

    command = command.lower().strip()

    if command in ["hello", "hi", "hey"]:
        return "GREETING"

    elif "time" in command:
        return "TIME_REQUEST"

    elif "date" in command:
        return "DATE_REQUEST"

    elif "help" in command:
        return "HELP"

    elif command == "exit":
        return "EXIT"

    else:
        return "UNKNOWN"