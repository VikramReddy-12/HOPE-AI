"""
HOPE Intent Detection Engine

This module detects the user's intent before the
request is sent to the Router.
"""


def detect_intent(command):
    """
    Detect the user's intent.

    Parameters:
        command (str): User input.

    Returns:
        str: Detected intent.
    """

    command = command.lower().strip()

    # Remove common punctuation
    command = (
        command.replace("?", "")
               .replace(".", "")
               .replace("!", "")
    )

    # -----------------------------
    # Greetings
    # -----------------------------
    if command in [
        "hello",
        "hi",
        "hey"
    ]:
        return "GREETING"

    # -----------------------------
    # Time / Date
    # -----------------------------
    elif "time" in command:
        return "TIME_REQUEST"

    elif "date" in command:
        return "DATE_REQUEST"

    # -----------------------------
    # Help
    # -----------------------------
    elif "help" in command:
        return "HELP"

    # -----------------------------
    # Conversation
    # -----------------------------
    elif command in [
        "what did i just say",
        "what was my last message",
        "repeat my last message"
    ]:
        return "LAST_USER_MESSAGE"

    elif command in [
        "what did we talk about",
        "summarize our conversation",
        "conversation summary",
        "summarize the conversation"
    ]:
        return "CONVERSATION_SUMMARY"

    # -----------------------------
    # Memory
    # -----------------------------
    elif command.startswith("remember "):
        return "MEMORY_SAVE"

    elif command.startswith("recall "):
        return "MEMORY_RECALL"

    # -----------------------------
    # Goal Detection
    # -----------------------------
    elif (
        command.startswith("i want to become ")
        or command.startswith("i want to be ")
        or command.startswith("i want to learn ")
        or command.startswith("my goal is ")
        or command.startswith("i want a career in ")
        or command.startswith("i want a job as ")
        or command.startswith("i would like to become ")
    ):
        return "GOAL"

    # -----------------------------
    # Goal Recall
    # -----------------------------
    elif command in [
        "what is my goal",
        "what's my goal",
        "show my goal",
        "my goal",
        "current goal"
    ]:
        return "GOAL_RECALL"

    # -----------------------------
    # Study Planner
    # -----------------------------
    elif command in [
        "what should i study today",
        "study plan",
        "today's study plan",
        "todays study plan",
        "create a study plan",
        "show my study plan",
        "plan my study",
        "what should i learn today"
    ]:
        return "STUDY_PLAN"

    # -----------------------------
    # Progress
    # -----------------------------
    elif command in [
        "show my progress",
        "my progress",
        "progress",
        "learning progress",
        "goal progress"
    ]:
        return "PROGRESS"

    # -----------------------------
    # Next Topic
    # -----------------------------
    elif command in [
        "what is my next topic",
        "what should i learn next",
        "next topic",
        "next lesson",
        "next step",
        "continue my roadmap"
    ]:
        return "NEXT_TOPIC"

    # -----------------------------
    # Mark Completed
    # -----------------------------
    elif (
        command.startswith("mark ")
        and command.endswith(" completed")
    ):
        return "MARK_COMPLETED"

    # -----------------------------
    # Comparison
    # -----------------------------
    elif (
        command.startswith("compare ")
        or command.startswith("compare between ")
        or command.startswith("difference between ")
        or command.startswith("difference of ")
        or " vs " in command
        or " versus " in command
        or " compare " in command
        or " or " in command
    ):
        return "COMPARE"

    # -----------------------------
    # Recommendation
    # -----------------------------
    elif (
        command.startswith("should i ")
        or command.startswith("recommend ")
        or command.startswith("which is better")
        or command.startswith("which language")
        or command.startswith("best language")
        or command.startswith("best programming language")
        or command.startswith("what should i learn")
        or command.startswith("which should i choose")
        or command.startswith("which one is better")
    ):
        return "RECOMMEND"

    # -----------------------------
    # Knowledge Search
    # -----------------------------
    elif (
        command.startswith("what is ")
        or command.startswith("what are ")
        or command.startswith("who is ")
        or command.startswith("who created ")
        or command.startswith("who invented ")
        or command.startswith("tell me about ")
        or command.startswith("explain ")
        or command.startswith("when was ")
        or command.startswith("when did ")
        or command.startswith("advantages of ")
        or command.startswith("disadvantages of ")
        or command.startswith("pros of ")
        or command.startswith("cons of ")
        or command.startswith("benefits of ")
        or command.startswith("drawbacks of ")
        or command.startswith("uses of ")
        or command.startswith("purpose of ")
        or command.startswith("best for ")
        or command.startswith("is ")
        or "used for" in command
        or "advantages" in command
        or "disadvantages" in command
        or "benefits" in command
        or "pros" in command
        or "cons" in command
        or "best for" in command
        or "beginner" in command
        or "easy" in command
        or "hard" in command
    ):
        return "KNOWLEDGE_SEARCH"

    # -----------------------------
    # Exit
    # -----------------------------
    elif command == "exit":
        return "EXIT"

    # -----------------------------
    # Unknown
    # -----------------------------
    else:
        return "UNKNOWN"