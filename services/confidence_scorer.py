def calculate_confidence(transcript: str, audio_duration: float) -> int:
    """
    Calculates confidence score (0–100) based on speech rate and length.
    """

    if not transcript or audio_duration <= 0:
        return 0

    words = transcript.split()
    word_count = len(words)

    words_per_second = word_count / audio_duration

    confidence = 0

    # Fluency score
    if words_per_second >= 2.0:
        confidence += 50
    elif words_per_second >= 1.2:
        confidence += 35
    else:
        confidence += 20

    # Content length score
    if word_count >= 40:
        confidence += 50
    elif word_count >= 20:
        confidence += 35
    else:
        confidence += 20

    return min(confidence, 100)
