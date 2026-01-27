from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.colors import lightgrey, Color
from reportlab.lib.utils import ImageReader
from datetime import datetime
import os
import uuid
import logging

from services.examiner_summary import generate_examiner_summary

logger = logging.getLogger(__name__)

LOGO_PATH = "assets/simats_engineering_logo.jpg"
WATERMARK_TEXT = "SIMATS ENGINEERING – OFFICIAL EXAM REPORT"
REPORT_DIR = "reports/generated_reports"
os.makedirs(REPORT_DIR, exist_ok=True)

def calculate_grade(percentage: float) -> str:
    if percentage >= 90: return "A+"
    elif percentage >= 80: return "A"
    elif percentage >= 70: return "B"
    elif percentage >= 60: return "C"
    return "F"

def draw_watermark(c, width, height):
    c.saveState()
    c.setFont("Helvetica-Bold", 42)
    c.setFillColor(Color(0.7, 0.7, 0.7, alpha=0.12))
    c.translate(width / 2, height / 2)
    c.rotate(45)
    c.drawCentredString(0, 0, WATERMARK_TEXT)
    c.restoreState()

def draw_header(c, width, height):
    draw_watermark(c, width, height)
    if os.path.exists(LOGO_PATH):
        try:
            c.drawImage(ImageReader(LOGO_PATH), 2*cm, height-3.5*cm, width=4.5*cm, preserveAspectRatio=True, mask='auto')
        except: pass

def draw_footer(c, page_no):
    c.setFont("Helvetica", 8)
    c.setFillColor(lightgrey)
    c.drawRightString(A4[0] - 2*cm, 1.5*cm, f"Page {page_no} | Official AI Viva Report")

def generate_viva_report(session_info: dict, answers: list) -> str:
    report_id = uuid.uuid4().hex
    file_path = os.path.join(REPORT_DIR, f"viva_report_{report_id}.pdf")
    c = canvas.Canvas(file_path, pagesize=A4)
    width, height = A4
    y = height - 4 * cm
    page_no = 1
    styles = getSampleStyleSheet()
    normal = styles["Normal"]
    normal.fontName = "Helvetica"; normal.fontSize = 10; normal.alignment = TA_LEFT

    def new_page():
        nonlocal y, page_no
        draw_footer(c, page_no)
        c.showPage()
        page_no += 1
        draw_header(c, width, height)
        y = height - 4 * cm

    def draw_text(text, size=10):
        nonlocal y
        if y < 2.5 * cm: new_page()
        c.setFont("Helvetica", size)
        c.drawString(2 * cm, y, text)
        y -= size + 6

    def draw_paragraph(text):
        nonlocal y
        para = Paragraph(text or "No answer transcript available.", normal)
        w, h = para.wrap(width - 4 * cm, height)
        if y - h < 2.5 * cm: new_page()
        para.drawOn(c, 2 * cm, y - h)
        y -= h + 6

    draw_header(c, width, height)
    draw_text("AI Voice Viva Examination Report", 15)
    draw_text("-" * 90)
    y -= 8
    draw_text(f"Student Name : {session_info.get('student_name', 'N/A')}")
    draw_text(f"Register No  : {session_info.get('register_no', 'N/A')}")
    draw_text(f"Subject      : {session_info.get('subject_name', 'N/A')}")
    draw_text(f"Date         : {datetime.now().strftime('%d %b %Y, %I:%M %p')}")
    y -= 15

    total_score = 0.0; total_max = 0.0
    for idx, ans in enumerate(answers, start=1):
        draw_text(f"Q{idx}. {ans.get('question', 'Question text missing')}", 11)
        draw_text("Transcript:")
        draw_paragraph(ans.get("transcript"))
        score = float(ans.get("score", 0)); m_score = float(ans.get("max_score", 1))
        draw_text(f"Marks : {score} / {m_score}")
        y -= 10
        total_score += score; total_max += m_score

    y -= 10
    draw_text("-" * 90)
    percentage = round((total_score / total_max * 100), 2) if total_max > 0 else 0
    grade = calculate_grade(percentage)
    draw_text(f"Total Score : {total_score} / {total_max}  ({percentage}%)", 12)
    draw_text(f"Final Grade : {grade}", 12)

    try:
        summary = generate_examiner_summary(percentage=percentage, grade=grade)
        y -= 10
        draw_text("Examiner Summary:", 11)
        draw_paragraph(summary)
    except: pass

    draw_footer(c, page_no)
    c.save()
    return file_path
