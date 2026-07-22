from assistant.router import route
from ai.brain import think


def chat():

    print()
    print("HOPE is ready to talk.")
    print("Type 'exit' to close HOPE.")
    print()

    while True:

        user = input("You: ")

        command, intent = think(user)

        if intent == "EXIT":
            print("HOPE: Goodbye Vikram!")
            print("HOPE: Shutting down...")
            break

        response = route(command, intent)

        print(f"HOPE: {response}")