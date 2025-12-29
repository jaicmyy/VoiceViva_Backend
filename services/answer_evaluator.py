def evaluate_answer(transcript: str, max_marks: int):
    """
    Simple length + clarity based scoring (LLM-free).
    """

    word_count = len(transcript.split())

    if word_count < 5:
        score = 0
    elif word_count < 20:
        score = max_marks * 0.4
    elif word_count < 40:
        score = max_marks * 0.7
    else:
        score = max_marks

    return round(score, 2)
