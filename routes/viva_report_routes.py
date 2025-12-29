from flask import Blueprint, send_file
import pymysql
from services.viva_report_generator import generate_viva_report

viva_report_bp = Blueprint("viva_report", __name__)


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )


@viva_report_bp.route("/api/viva/<int:session_id>/report", methods=["GET"])
def generate_report(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Session info
    cursor.execute(
        """
        SELECT s.student_name, s.register_no, sub.subject_name
        FROM viva_sessions s
        JOIN subjects sub ON s.subject_id = sub.id
        WHERE s.id=%s
        """,
        (session_id,)
    )
    session_info = cursor.fetchone()

    # Answers
    cursor.execute(
        """
        SELECT q.question_text AS question,
               a.transcript,
               a.score,
               a.max_score,
               a.confidence
        FROM answers a
        JOIN questions q ON a.question_id = q.id
        WHERE a.session_id=%s
        """,
        (session_id,)
    )
    answers = cursor.fetchall()

    cursor.close()
    conn.close()

    pdf_path = generate_viva_report(session_info, answers)
    return send_file(pdf_path, as_attachment=True)
