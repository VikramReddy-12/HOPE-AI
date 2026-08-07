"""
HOPE Progress Engine

Tracks the user's learning progress for each goal.

Features:
- Save completed topics
- Retrieve completed topics
- Find the next topic
- Calculate completion percentage
"""

from memory.storage import load_memory, save_memory
from goal.roadmap import get_roadmap


def _get_roadmap_topics(goal):
    """
    Extract learning topics from the roadmap.
    """

    roadmap = get_roadmap(goal)

    if roadmap is None:
        return []

    topics = []

    for line in roadmap.splitlines():

        line = line.strip()

        if len(line) >= 2 and line[0].isdigit():

            try:
                topic = line.split(".", 1)[1].strip()
                topics.append(topic)
            except IndexError:
                pass

    return topics


def get_completed_topics(goal):
    """
    Return completed topics for the goal.
    """

    memory = load_memory()

    progress = memory.get("goal_progress", {})

    return progress.get(goal, [])


def mark_completed(goal, topic):
    """
    Mark a topic as completed.
    """

    memory = load_memory()

    progress = memory.get("goal_progress", {})

    completed = progress.get(goal, [])

    if topic not in completed:
        completed.append(topic)

    progress[goal] = completed

    memory["goal_progress"] = progress

    save_memory(memory)

    return f"Completed: {topic}"


def get_next_topic(goal):
    """
    Return the next unfinished topic.
    """

    roadmap_topics = _get_roadmap_topics(goal)

    completed = get_completed_topics(goal)

    for topic in roadmap_topics:

        if topic not in completed:
            return topic

    return None


def get_completion_percentage(goal):
    """
    Calculate completion percentage.
    """

    roadmap_topics = _get_roadmap_topics(goal)

    if not roadmap_topics:
        return 0

    completed = get_completed_topics(goal)

    percentage = (
        len(completed) / len(roadmap_topics)
    ) * 100

    return round(percentage)


def get_progress(goal):
    """
    Return formatted progress report.
    """

    roadmap_topics = _get_roadmap_topics(goal)

    completed = get_completed_topics(goal)

    next_topic = get_next_topic(goal)

    percentage = get_completion_percentage(goal)

    response = []

    response.append(f"🎯 Goal: {goal}")
    response.append("")
    response.append(f"Progress: {percentage}%")
    response.append("")

    response.append("Completed Topics:")

    if completed:

        for topic in completed:
            response.append(f"✓ {topic}")

    else:

        response.append("None")

    response.append("")

    if next_topic:

        response.append(f"Next Topic: {next_topic}")

    else:

        response.append("🎉 Congratulations!")
        response.append("You have completed this roadmap.")

    return "\n".join(response)