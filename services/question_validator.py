def is_valid_question(text):
    if not text:
        return False

    text = text.strip()

    # Must be a question
    if not text.endswith("?"):
        return False

    # Minimum length
    if len(text.split()) < 4:
        return False

    return True


def normalize_difficulty(level):
    if level not in ["easy", "medium", "hard"]:
        return "medium"
    return level
