from assistant.router import route
from ai.brain import think


def chat():

    print()
    print("HOPE is ready to talk.")
    print("Type 'exit' to close HOPE.")
    print()

    while True:

        user = input("You: ")

        result = think(user)

        intent = result["intent"]

        if intent == "EXIT":
            print("HOPE: Goodbye Vikram!")
            print("HOPE: Shutting down...")
            break

        response = route(result)

        print(f"HOPE: {response}")