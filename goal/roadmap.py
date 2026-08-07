"""
HOPE Goal Roadmap Engine

Provides structured learning roadmaps
for supported user goals.
"""

ROADMAPS = {

    "Ai Engineer": {
        "duration": "8-12 months",
        "steps": [
            "Learn Python",
            "Master Git & GitHub",
            "Learn Data Structures and Algorithms",
            "Learn SQL",
            "Study Machine Learning",
            "Study Deep Learning",
            "Build AI Projects",
            "Create a Professional Resume",
            "Apply for AI Engineer Jobs"
        ]
    },

    "Software Engineer": {
        "duration": "6-10 months",
        "steps": [
            "Learn Python or Java",
            "Master Data Structures",
            "Learn Git & GitHub",
            "Practice Problem Solving",
            "Build Full Stack Projects",
            "Learn Databases",
            "Prepare Resume",
            "Practice Interviews",
            "Apply for Software Engineer Jobs"
        ]
    },

    "Python": {
        "duration": "2-3 months",
        "steps": [
            "Python Basics",
            "Functions",
            "Object-Oriented Programming",
            "File Handling",
            "Modules",
            "Projects"
        ]
    },

    "Java": {
        "duration": "3-4 months",
        "steps": [
            "Java Basics",
            "OOP Concepts",
            "Collections",
            "Exception Handling",
            "Multithreading",
            "Projects"
        ]
    }
}


def get_roadmap(goal):
    """
    Return the roadmap for a goal.

    Parameters:
        goal (str)

    Returns:
        str
    """

    if goal not in ROADMAPS:
        return (
            f"Sorry, I don't have a roadmap for '{goal}' yet."
        )

    roadmap = ROADMAPS[goal]

    response = []

    response.append(f"🎯 Goal: {goal}")
    response.append("")
    response.append(f"Estimated Duration: {roadmap['duration']}")
    response.append("")
    response.append("Learning Roadmap:")

    for index, step in enumerate(roadmap["steps"], start=1):
        response.append(f"{index}. {step}")

    return "\n".join(response)