"""
HOPE Command Processing Engine

Handles basic system commands and CLI responses
for the HOPE AI assistant.
"""

from datetime import datetime

from core.system import (
    get_about,
    get_system_version,
    get_system_copyright,
)

from core.help import show_help


# ============================================================
# MAIN COMMAND PROCESSOR
# ============================================================

def process_command(user):
    """
    Process basic HOPE system commands.

    Parameters:
        user (str): User input.

    Returns:
        str: Command response.
    """

    # --------------------------------------------------------
    # None Input
    # --------------------------------------------------------

    if user is None:
        return "Please enter a command."

    command = user.lower().strip()

    # --------------------------------------------------------
    # Empty Input
    # --------------------------------------------------------

    if not command:
        return "Please enter a command."

    # --------------------------------------------------------
    # Greeting
    # --------------------------------------------------------

    if command in [
        "hello",
        "hi",
        "hey",
        "hey hope",
        "hello hope",
    ]:
        return "Hello Vikram!"

    # --------------------------------------------------------
    # General Conversation
    # --------------------------------------------------------

    elif command in [
        "how are you",
        "how are you doing",
    ]:
        return "I am doing great!"

    # --------------------------------------------------------
    # Time
    # --------------------------------------------------------

    elif command in [
        "time",
        "what time is it",
        "current time",
    ]:
        return datetime.now().strftime("%I:%M:%S %p")

    # --------------------------------------------------------
    # Date
    # --------------------------------------------------------

    elif command in [
        "date",
        "what is today's date",
        "what is todays date",
        "today's date",
        "todays date",
        "current date",
    ]:
        return datetime.now().strftime("%d %B %Y")

    # --------------------------------------------------------
    # About
    # --------------------------------------------------------

    elif command in [
        "about",
        "about hope",
        "about hope ai",
        "who are you",
    ]:
        return get_about()

    # --------------------------------------------------------
    # Version
    # --------------------------------------------------------

    elif command in [
        "version",
        "show version",
        "current version",
        "what version are you",
    ]:
        return get_system_version()

    # --------------------------------------------------------
    # Copyright
    # --------------------------------------------------------

    elif command in [
        "copyright",
        "show copyright",
    ]:
        return get_system_copyright()

    # --------------------------------------------------------
    # Help
    # --------------------------------------------------------

    elif command in [
        "help",
        "commands",
        "show commands",
        "available commands",
    ]:
        return show_help()

    # --------------------------------------------------------
    # Exit
    # --------------------------------------------------------

    elif command in [
        "exit",
        "quit",
        "bye",
    ]:
        return "Goodbye!"

    # --------------------------------------------------------
    # Unknown Command
    # --------------------------------------------------------

    else:
        return (
            "Sorry, I don't understand that yet.\n"
            "Type 'help' to see available commands."
        )