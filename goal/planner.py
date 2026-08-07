"""
HOPE Goal Planner

Generates personalized study plans
based on the user's progress.
"""

from goal.progress import get_next_topic


def estimate_study_time():
    """
    Estimate study time.
    """

    return "2 Hours"


def get_today_plan(goal):
    """
    Generate today's study plan.
    """

    topic = get_next_topic(goal)

    if topic is None:

        return (
            "🎉 Congratulations!\n\n"
            "You have completed your roadmap."
        )

    response = []

    response.append("📚 Today's Study Plan")
    response.append("")
    response.append(f"🎯 Goal: {goal}")
    response.append("")
    response.append("Today's Focus")
    response.append("")
    response.append(f"• {topic}")
    response.append("• Take notes")
    response.append("• Practice what you learned")
    response.append("• Review yesterday's concepts")
    response.append("")
    response.append(
        f"Estimated Time: {estimate_study_time()}"
    )

    return "\n".join(response)