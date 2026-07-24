import re


def understand(text):
    """
    Understand simple natural language.
    Returns:
        dict or None
    """

    text = text.strip()

    # Pattern:
    # My favorite car is BMW 7 Series

    match = re.match(
        r"my favorite car is (.+)",
        text,
        re.IGNORECASE
    )

    if match:

        return {
            "intent": "MEMORY_SAVE",
            "key": "favorite_car",
            "value": match.group(1)
        }

    return None