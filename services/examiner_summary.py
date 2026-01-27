def generate_examiner_summary(
    percentage: float,
    grade: str,
    avg_confidence: float = 0.0
) -> str:
    """
    Generates a professional examiner-style summary paragraph.
    """

    if percentage >= 75:
        performance = "demonstrated strong conceptual clarity and confidence"
    elif percentage >= 50:
        performance = "showed moderate understanding with some conceptual gaps"
    else:
        performance = "displayed insufficient understanding of core concepts"

    confidence_text = ""
    if avg_confidence > 70:
        confidence_text = " The candidate was very expressive and confident in their delivery."
    elif avg_confidence < 40:
        confidence_text = " However, the delivery lacked confidence and had significant pauses."

    return (
        f"The candidate {performance}. "
        f"The overall performance corresponds to grade {grade}."
        f"{confidence_text} "
        "Responses indicate the current level of preparedness for the subject."
    )
