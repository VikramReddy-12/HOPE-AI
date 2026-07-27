from assistant.router import route
from ai.brain import think
from conversation.manager import add_message


def chat():

    print()
    print("HOPE is ready to talk.")
    print("Type 'exit' to close HOPE.")
    print()

    while True:

        user = input("You: ")

        # Save the user's message
        add_message("user", user)

        # Send the message to the Brain
        result = think(user)

        intent = result["intent"]

        # Exit command
        if intent == "EXIT":
            print("HOPE: Goodbye Vikram!")
            print("HOPE: Shutting down...")
            break

        # Get HOPE's response
        response = route(result)

        # Save HOPE's response
        add_message("hope", response)

        # Display the response
        print(f"HOPE: {response}")