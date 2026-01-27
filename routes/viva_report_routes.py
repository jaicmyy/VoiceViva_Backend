from flask import Blueprint, send_file, jsonify
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
        SELECT u.name AS student_name, u.registration_number AS register_no, sub.name AS subject_name
        FROM viva_sessions s
        JOIN users u ON s.student_id = u.id
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
               a.max_score
        FROM viva_answers a
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


@viva_report_bp.route("/api/admin/reports", methods=["GET"])
def get_all_reports():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Optimized Query: NO Python Loop for calculations
    # Relies on viva_reports table which is populated on submit.
    cursor.execute(
        """
        SELECT 
            vs.id,
            u.name AS student_name,
            u.registration_number,
            sub.name AS subject_name,
            
            COALESCE(vr.total_questions, 0) as total_questions,
            COALESCE(vr.max_total_score, 0) as max_score,
            CAST(COALESCE(vr.total_score, 0) AS UNSIGNED) AS score,
            COALESCE(vr.percentage, 0) AS percentage,
            
            CASE 
                WHEN vs.started_at IS NOT NULL THEN DATE_FORMAT(vs.started_at, '%Y-%m-%d %H:%i:%S')
                ELSE 'N/A'
            END as created_at
            
        FROM viva_sessions vs
        JOIN users u ON vs.student_id = u.id
        JOIN subjects sub ON vs.subject_id = sub.id
        LEFT JOIN viva_reports vr ON vs.id = vr.session_id
        ORDER BY vs.started_at DESC
        """
    )
    
    reports = cursor.fetchall()
    
    cursor.close()
    conn.close()
            
    return jsonify(reports), 200
