from memory.storage import load_memory, save_memory


def remember(key, value):
    """
    Save a piece of information.
    """

    memory = load_memory()

    memory[key] = value

    save_memory(memory)

    return f"I'll remember that your {key} is {value}."


def recall(key):
    """
    Recall saved information.
    """

    memory = load_memory()

    if key in memory:
        return memory[key]

    return None