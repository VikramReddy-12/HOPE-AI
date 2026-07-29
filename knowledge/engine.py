from knowledge.database import knowledge


def search_knowledge(question):
    """
    Searches the knowledge database for a matching topic.
    """

    question = question.lower()

    # Search every topic in the knowledge base
    for topic, answer in knowledge.items():

        if topic in question:
            return answer

    return "I don't know that yet."