"""
HOPE Intent Detection Engine

Detects user intent from natural language commands.

Supported intent groups:

- Basic conversation
- System commands
- Health and diagnostics
- Recovery
- Recovery history
- Recovery intelligence
- Recovery patterns
- Recovery trends
- Predictive failure intelligence
- Memory
- Goals
- Study planning
- Progress
- Conversation
- Knowledge
- Reasoning
- Exit
"""


def detect_intent(command):
    """
    Detect the intent of a user command.

    Parameters:
        command (str): User input.

    Returns:
        str: Detected intent.
    """

    # ========================================================
    # NORMALIZE COMMAND
    # ========================================================

    if command is None:

        return "UNKNOWN"

    command = str(
        command
    ).strip().lower()

    if not command:

        return "UNKNOWN"

    # ========================================================
    # EXIT
    # ========================================================

    if command in [
        "exit",
        "quit",
        "bye",
        "goodbye",
        "close",
        "shutdown",
    ]:

        return "EXIT"

    # ========================================================
    # GREETING
    # ========================================================

    if command in [
        "hi",
        "hello",
        "hey",
        "hey hope",
        "hello hope",
        "hi hope",
        "good morning",
        "good afternoon",
        "good evening",
    ]:

        return "GREETING"

    # ========================================================
    # TIME
    # ========================================================

    if command in [
        "time",
        "what time is it",
        "current time",
        "tell me the time",
    ]:

        return "TIME_REQUEST"

    # ========================================================
    # DATE
    # ========================================================

    if command in [
        "date",
        "what is the date",
        "today's date",
        "todays date",
        "current date",
        "tell me the date",
    ]:

        return "DATE_REQUEST"

    # ========================================================
    # ABOUT
    # ========================================================

    if command in [
        "about",
        "about hope",
        "who are you",
        "what are you",
        "tell me about yourself",
    ]:

        return "ABOUT"

    # ========================================================
    # VERSION
    # ========================================================

    if command in [
        "version",
        "hope version",
        "what version are you",
        "current version",
    ]:

        return "VERSION"

    # ========================================================
    # COPYRIGHT
    # ========================================================

    if command in [
        "copyright",
        "who created you",
        "who made you",
        "who is your creator",
    ]:

        return "COPYRIGHT"

    # ========================================================
    # HELP
    # ========================================================

    if command in [
        "help",
        "commands",
        "show commands",
        "available commands",
    ]:

        return "HELP"

    if command.startswith(
        "help "
    ):

        return "HELP"

    # ========================================================
    # RECOVERY INTELLIGENCE
    # ========================================================

    if command in [
        "recovery intelligence",
        "recovery analysis",
        "recovery statistics",
        "recovery insights",
        "recovery recommendation",
        "problem modules",
    ]:

        return "RECOVERY_INTELLIGENCE"

    # ========================================================
    # RECOVERY PATTERN INTELLIGENCE
    # ========================================================

    if command in [
        "recovery patterns",
        "recovery pattern",
        "module reliability",
        "failure patterns",
    ]:

        return "RECOVERY_PATTERNS"

    # ========================================================
    # RECOVERY TREND INTELLIGENCE
    # ========================================================

    if command in [
        "recovery trend",
        "recovery trends",
        "recovery trend analysis",
        "recovery frequency",
    ]:

        return "RECOVERY_TRENDS"

    # ========================================================
    # PREDICTIVE FAILURE INTELLIGENCE
    # ========================================================

    if command in [
        "predict failures",
        "failure prediction",
        "predictive failure",
        "failure risk",
        "module risk",
        "risk analysis",
        "predict recovery failures",
    ]:

        return "PREDICTIVE_FAILURE"

    # ========================================================
    # RECOVERY HISTORY
    # ========================================================

    if command in [
        "recovery history",
        "show recovery history",
        "recovery log",
        "show recovery log",
    ]:

        return "RECOVERY_HISTORY"

    # ========================================================
    # LAST RECOVERY
    # ========================================================

    if command in [
        "last recovery",
        "what was the last recovery",
        "show last recovery",
        "latest recovery",
        "last recovery event",
    ]:

        return "LAST_RECOVERY"

    # ========================================================
    # PREDICTIVE INTELLIGENCE
    # ========================================================

    if command in [
        "predictive status",
        "show predictive status",
        "check predictive status",
        "prediction status",
        "show prediction status",
        "hope predictive status",
    ]:

        return "PREDICTIVE_STATUS"

    # ========================================================
    # PREDICTIVE RISK
    # ========================================================

    if command in [
        "predictive risk",
        "system risk",
        "check system risk",
        "what is the system risk",
        "what is the predictive risk",
        "is there any predictive risk",
        "current predictive risk",
        "show predictive risk",
    ]:

        return "PREDICTIVE_RISK"

    # ========================================================
    # PREDICTIVE REPORT
    # ========================================================

    if command in [
        "predictive report",
        "show predictive report",
        "complete predictive report",
        "full predictive report",
        "predictive intelligence report",
        "show predictive intelligence report",
        "predictive analysis report",
        "show predictive analysis",
    ]:

        return "PREDICTIVE_REPORT"

    # ========================================================
    # MODULE RISK
    # ========================================================

    if command in [
        "module risk",
        "module risks",
        "show module risk",
        "show module risks",
        "which module is at risk",
        "which module needs attention",
        "which engine is at risk",
        "which engine needs attention",
        "highest risk module",
        "highest risk engine",
    ]:

        return "MODULE_RISK"

    # ========================================================
    # PREDICTIVE SYSTEM HEALTH
    # ========================================================

    if command in [
        "predictive health",
        "predictive system health",
        "check predictive health",
        "is hope predictively healthy",
        "predictive health status",
    ]:

        return "SYSTEM_HEALTH"

    # ========================================================
    # PREDICTIVE DECISION
    # ========================================================

    if command in [
        "predictive decision",
        "show predictive decision",
        "show predictive decisions",
        "predictive action decision",
        "predictive action decisions",
        "show predictive action decision",
        "show predictive action decisions",
        "what should hope do about the risk",
        "what should we do about the risk",
        "what should we do about the knowledge engine",
        "what action should be taken",
        "show predictive actions",
    ]:
        return "PREDICTIVE_DECISION"

    # ========================================================
    # PREDICTIVE RECOMMENDATION
    # ========================================================

    if command in [
        "predictive recommendation",
        "predictive recommendations",
        "what does hope recommend about the risk",
        "what should i do about the system risk",
        "what action should i take about the risk",
        "what action should hope take",
        "which module should i investigate",
        "what should i investigate",
    ]:

        return "PREDICTIVE_RECOMMENDATION"

    # ========================================================
    # PREDICTIVE EXPLANATION
    # ========================================================

    if (
        command in [
            "predictive explanation",
            "predictive explanations",
            "explain predictive risk",
            "explain the predictive risk",
            "why is the system at risk",
            "why is the system risky",
            "why is the module at risk",
            "why is this module at risk",
            "why is the knowledge engine at risk",
            "why is the brain engine at risk",
            "why is the context engine at risk",
            "why is the goal engine at risk",
            "why is the memory engine at risk",
            "why is the planner engine at risk",
            "why is the progress engine at risk",
            "why is the reasoning engine at risk",
            "why is knowledge engine at risk",
            "why is brain engine at risk",
            "why is context engine at risk",
            "why is goal engine at risk",
            "why is memory engine at risk",
            "why is planner engine at risk",
            "why is progress engine at risk",
            "why is reasoning engine at risk",
        ]
        or command.startswith("why is ")
        and " at risk" in command
        or command.startswith("explain predictive")
    ):

        return "PREDICTIVE_EXPLANATION"

    # ========================================================
    # AUTOMATIC RECOVERY
    # ========================================================

    if command in [
        "recover",
        "auto recover",
        "automatic recovery",
        "recover system",
        "run recovery",
        "repair hope",
        "fix system",
    ]:

        return "RECOVERY"

    # ========================================================
    # HEALTH
    # ========================================================

    if command in [
        "health",
        "system health",
        "health check",
        "check health",
        "is hope healthy",
    ]:

        return "HEALTH"

    # ========================================================
    # STATUS
    # ========================================================

    if command in [
        "status",
        "system status",
        "current status",
        "hope status",
    ]:

        return "STATUS"

    # ========================================================
    # DIAGNOSTICS
    # ========================================================

    if command in [
        "diagnostics",
        "system diagnostics",
        "run diagnostics",
        "check system",
    ]:

        return "STATUS"

    # ========================================================
    # MEMORY SAVE
    # ========================================================

    if command.startswith(
        "remember "
    ):

        return "MEMORY_SAVE"

    if command.startswith(
        "save memory "
    ):

        return "MEMORY_SAVE"

    # ========================================================
    # MEMORY RECALL
    # ========================================================

    if command.startswith(
        "recall "
    ):

        return "MEMORY_RECALL"

    if command.startswith(
        "remember what "
    ):

        return "MEMORY_RECALL"

    # ========================================================
    # GOAL RECALL
    # ========================================================

    if command in [
        "my goal",
        "current goal",
        "what is my goal",
        "show my goal",
        "what's my goal",
        "recall my goal",
    ]:

        return "GOAL_RECALL"

    # ========================================================
    # STUDY PLAN
    # ========================================================

    if command in [
        "today plan",
        "today's plan",
        "todays plan",
        "study plan",
        "my plan",
        "today study plan",
        "what should i study",
        "what should i learn today",
    ]:

        return "STUDY_PLAN"

    # ========================================================
    # PROGRESS
    # ========================================================

    if command in [
        "progress",
        "my progress",
        "show progress",
        "check progress",
        "goal progress",
    ]:

        return "PROGRESS"

    # ========================================================
    # NEXT TOPIC
    # ========================================================

    if command in [
        "next topic",
        "what next",
        "what should i learn next",
        "next",
        "next step",
    ]:

        return "NEXT_TOPIC"

    # ========================================================
    # MARK COMPLETED
    # ========================================================

    if (
        command.startswith("mark ")
        and command.endswith(" completed")
    ):

        return "MARK_COMPLETED"

    # ========================================================
    # GOAL DETECTION
    # ========================================================

    goal_phrases = [
        "i want to",
        "my goal is",
        "i want",
        "my target is",
        "i plan to",
        "i need to become",
        "i would like to become",
    ]

    for phrase in goal_phrases:

        if command.startswith(
            phrase
        ):

            return "GOAL"

    # ========================================================
    # LAST USER MESSAGE
    # ========================================================

    if command in [
        "what did i say",
        "what did i just say",
        "what was my last message",
        "last message",
        "my last message",
        "what did i tell you",
    ]:

        return "LAST_USER_MESSAGE"

    # ========================================================
    # CONVERSATION SUMMARY
    # ========================================================

    if command in [
        "summary",
        "conversation summary",
        "summarize conversation",
        "summarize our conversation",
        "what did we talk about",
        "summarize our chat",
    ]:

        return "CONVERSATION_SUMMARY"

    # ========================================================
    # COMPARISON
    # ========================================================

    if (
        command.startswith("compare ")
        or " vs " in command
        or " versus " in command
        or command.startswith("difference between ")
    ):

        return "COMPARE"

    # ========================================================
    # RECOMMENDATION
    # ========================================================

    if (
        command.startswith("recommend ")
        or command.startswith("recommendation ")
        or command.startswith("suggest ")
        or command.startswith("which is better ")
        or command.startswith("what should i buy ")
        or command.startswith("what should i choose ")
    ):

        return "RECOMMEND"

    # ========================================================
    # KNOWLEDGE SEARCH
    # ========================================================

    knowledge_phrases = [
        "what is ",
        "what are ",
        "who is ",
        "tell me about ",
        "explain ",
        "information about ",
        "info about ",
        "how does ",
        "why does ",
        "why is ",
        "define ",
    ]

    for phrase in knowledge_phrases:

        if command.startswith(
            phrase
        ):

            return "KNOWLEDGE_SEARCH"

    # ========================================================
    # UNKNOWN
    # ========================================================

    # ========================================================
    # MEMORY FORGET
    # ========================================================

    # Detect explicit memory-removal commands before the generic
    # UNKNOWN fallback.
    if command.startswith("forget "):
        return "FORGET"

    if command.startswith("delete memory "):
        return "FORGET"

    if command.startswith("remove memory "):
        return "FORGET"

    return "UNKNOWN"