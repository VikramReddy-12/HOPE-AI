from datetime import datetime

def process_command(user):

    command = user.lower().strip()

    if command == "hello":
        return "Hello Vikram!"

    elif command == "how are you":
        return "I am doing great!"

    elif command == "time":
        return datetime.now().strftime("%I:%M:%S %p")

    elif command == "date":
        return datetime.now().strftime("%d %B %Y")

    elif command == "help":
        return (
            "Available commands:\n"
            "- hello\n"
            "- how are you\n"
            "- time\n"
            "- date\n"
            "- help\n"
            "- exit"
        )

    else:
        return "Sorry, I don't understand that yet."