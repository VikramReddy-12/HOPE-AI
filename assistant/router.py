"""
HOPE Router

Routes the detected intent to the
appropriate HOPE module.
"""

from assistant.commands import process_command

from memory.manager import remember, recall

from conversation.manager import get_last_user_message
from conversation.summary import summarize_conversation

from knowledge.engine import search_knowledge

from reasoning.engine import reason

from goal.engine import process_goal
from goal.roadmap import get_roadmap
from goal.planner import get_today_plan
from goal.progress import (
    get_progress,
    get_next_topic,
    mark_completed
)


def route(result):
    """
    Route the detected intent to the
    appropriate module.
    """

    intent = result["intent"]

    print(f"[Router] Intent : {intent}")

    # -----------------------------
    # Greetings
    # -----------------------------
    if intent == "GREETING":
        return process_command(result["command"])

    # -----------------------------
    # Time
    # -----------------------------
    elif intent == "TIME_REQUEST":
        return process_command(result["command"])

    # -----------------------------
    # Date
    # -----------------------------
    elif intent == "DATE_REQUEST":
        return process_command(result["command"])

    # -----------------------------
    # Help
    # -----------------------------
    elif intent == "HELP":
        return process_command(result["command"])

    # -----------------------------
    # Memory Save
    # -----------------------------
    elif intent == "MEMORY_SAVE":

        if "key" in result and "value" in result:

            key = result["key"]
            value = result["value"]

        else:

            command = result["command"]

            parts = command.split(" ", 2)

            if len(parts) != 3:
                return "Usage: remember <key> <value>"

            key = parts[1]
            value = parts[2]

        print("[Router] Saving Memory")
        print(f"[Router] Key   : {key}")
        print(f"[Router] Value : {value}")

        return remember(key, value)

    # -----------------------------
    # Memory Recall
    # -----------------------------
    elif intent == "MEMORY_RECALL":

        command = result["command"]

        parts = command.split(" ", 1)

        if len(parts) == 2:

            key = parts[1]

            print("[Router] Recalling Memory")
            print(f"[Router] Key : {key}")

            value = recall(key)

            if value:
                return value

            return "I don't remember that."

        return "Usage: recall <key>"

    # -----------------------------
    # Goal Detection
    # -----------------------------
    elif intent == "GOAL":

        command = result["command"]

        goal_result = process_goal(command)

        if goal_result is None:
            return "I couldn't identify your goal."

        goal = goal_result["goal"]

        return get_roadmap(goal)

    # -----------------------------
    # Goal Recall
    # -----------------------------
    elif intent == "GOAL_RECALL":

        goal = recall("current_goal")

        if goal is None:
            return "You haven't told me your goal yet."

        return f"🎯 Your current goal is:\n\n{goal}"

    # -----------------------------
    # Study Plan
    # -----------------------------
    elif intent == "STUDY_PLAN":

        goal = recall("current_goal")

        if goal is None:
            return (
                "You haven't set a goal yet.\n\n"
                "Try saying:\n"
                "'I want to become AI Engineer'"
            )

        return get_today_plan(goal)

    # -----------------------------
    # Progress
    # -----------------------------
    elif intent == "PROGRESS":

        goal = recall("current_goal")

        if goal is None:
            return "You haven't set a goal yet."

        return get_progress(goal)

    # -----------------------------
    # Next Topic
    # -----------------------------
    elif intent == "NEXT_TOPIC":

        goal = recall("current_goal")

        if goal is None:
            return "You haven't set a goal yet."

        topic = get_next_topic(goal)

        if topic is None:
            return (
                "🎉 Congratulations!\n"
                "You have completed your roadmap."
            )

        return (
            "📘 Your next topic is:\n\n"
            f"{topic}"
        )

    # -----------------------------
    # Mark Completed
    # -----------------------------
    elif intent == "MARK_COMPLETED":

        goal = recall("current_goal")

        if goal is None:
            return "You haven't set a goal yet."

        command = result["command"]

        topic = (
            command.replace("mark", "")
                   .replace("completed", "")
                   .strip()
                   .title()
        )

        message = mark_completed(goal, topic)

        progress = get_progress(goal)

        return (
            f"{message}\n\n{progress}"
        )

    # -----------------------------
    # Conversation
    # -----------------------------
    elif intent == "LAST_USER_MESSAGE":

        last_message = get_last_user_message(skip_current=True)

        if last_message:
            return f'You said: "{last_message}"'

        return "I don't remember you saying anything yet."

    elif intent == "CONVERSATION_SUMMARY":

        return summarize_conversation()

    # -----------------------------
    # Knowledge Search
    # -----------------------------
    elif intent == "KNOWLEDGE_SEARCH":

        command = result["command"]

        response = reason(command)

        if response is not None:
            return response

        return search_knowledge(command)

    # -----------------------------
    # Comparison
    # -----------------------------
    elif intent == "COMPARE":

        command = result["command"]

        response = reason(command)

        if response is not None:
            return response

        return "I couldn't compare those topics."

    # -----------------------------
    # Recommendation
    # -----------------------------
    elif intent == "RECOMMEND":

        command = result["command"]

        response = reason(command)

        if response is not None:
            return response

        return "I don't have a recommendation."

    # -----------------------------
    # Exit
    # -----------------------------
    elif intent == "EXIT":

        return "Goodbye!"

    # -----------------------------
    # Unknown
    # -----------------------------
    else:

        command = result.get("command", "")

        return process_command(command)