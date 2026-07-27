from conversation.manager import (
    add_message,
    get_last_message,
    get_conversation,
    clear_conversation
)

clear_conversation()

add_message("user", "Hello")
add_message("hope", "Hello Vikram!")

print("Last Message:")
print(get_last_message())

print()

print("Conversation:")
print(get_conversation())