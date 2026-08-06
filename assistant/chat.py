"""
HOPE Chat Module

Handles the main conversation loop between
the user and HOPE.
"""

from assistant.router import route
from ai.brain import think
from conversation.manager import add_message


def chat():
    """
    Main chat loop.
    """

    while True:

        user = input("You: ").strip()

        # ---------------------------------
        # Empty input
        # ---------------------------------
        if not user:
            print("HOPE: Please enter a question.")
            continue

        # Save the user's message
        add_message("user", user)

        # Send the message to the Brain
        result = think(user)

        intent = result["intent"]

        # ---------------------------------
        # Exit
        # ---------------------------------
        if intent == "EXIT":
            print("HOPE: Goodbye Vikram!")
            print("HOPE: Shutting down...")
            break

        # ---------------------------------
        # Route request
        # ---------------------------------
        response = route(result)

        # Save HOPE's response
        add_message("hope", response)

        # Display response
        print(f"HOPE: {response}")