from assistant.action_dispatcher import dispatch
from ai.brain import think
from conversation.manager import add_message
from core.runtime_adapter import adapt_runtime


def chat():
    """
    Main chat loop.
    """
    while True:
        user = input("You: ").strip()

        if not user:
            print("HOPE: Please enter a question.")
            continue

        add_message("user", user)
        result = think(user)
        intent = result["intent"]

        if intent == "EXIT":
            print("HOPE: Goodbye Vikram!")
            print("HOPE: Shutting down...")
            break

        result = adapt_runtime(result)
        response = dispatch(result)
        add_message("hope", response)
        print(f"HOPE: {response}")
