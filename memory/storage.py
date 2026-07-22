import json
from pathlib import Path

# Path to HOPE's memory file
MEMORY_FILE = Path(__file__).parent / "data.json"


def load_memory():
    """
    Load all saved memories from data.json.
    Returns a dictionary.
    """

    if not MEMORY_FILE.exists():
        return {}

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_memory(data):
    """
    Save all memories into data.json.
    """

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)