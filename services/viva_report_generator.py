from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from datetime import datetime
import os
import uuid


REPORT_DIR = "reports/generated_reports"
os.makedirs(REPORT_DIR, exist_ok=True)


def generate_viva_report(session_info, answers):
    """
    session_info: dict with student_name, register_no, subject_name
    answers: list of dicts (question, transcript, score, max_score, confidence)
    """

    report_id = str(uuid.uuid4())
    file_path = f"{REPORT_DIR}/viva_report_{report_id}.pdf"

    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4

    y = height - 2 * cm

    def draw(text, size=10):
        nonlocal y
        c.setFont("Helvetica", size)
        c.drawString(2 * cm, y, text)
        y -= size + 4
        if y < 2 * cm:
            c.showPage()
            y = height - 2 * cm

    # ---------- HEADER ----------
    draw("AI Voice Viva Examination Report", 14)
    draw("=" * 60)
    y -= 10

    draw(f"Student Name : {session_info['student_name']}")
    draw(f"Register No  : {session_info['register_no']}")
    draw(f"Subject      : {session_info['subject_name']}")
    draw(f"Date         : {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    y -= 15

    # ---------- QUESTIONS ----------
    total_score = 0
    total_max = 0
    confidence_sum = 0

    for idx, ans in enumerate(answers, start=1):
        draw(f"Q{idx}. {ans['question']}", 11)
        draw(f"Answer    : {ans['transcript']}")
        draw(f"Marks     : {ans['score']} / {ans['max_score']}")
        draw(f"Confidence: {ans['confidence']}%")
        y -= 10

        total_score += ans["score"]
        total_max += ans["max_score"]
        confidence_sum += ans["confidence"]

    avg_confidence = round(confidence_sum / len(answers), 2) if answers else 0

    # ---------- SUMMARY ----------
    y -= 15
    draw("=" * 60)
    draw("SUMMARY", 12)
    y -= 5

    draw(f"Total Score       : {total_score} / {total_max}")
    draw(f"Average Confidence: {avg_confidence}%")

    if avg_confidence >= 75:
        draw("Overall Performance: Confident and clear responses")
    elif avg_confidence >= 50:
        draw("Overall Performance: Moderate confidence")
    else:
        draw("Overall Performance: Needs improvement in articulation")

    c.save()
    return file_path
