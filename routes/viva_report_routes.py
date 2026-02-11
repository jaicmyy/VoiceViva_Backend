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
            
            -- Dynamic Total Questions (Count items in comma-separated lists)
            (
               IF(vs.easy_q_ids IS NULL OR vs.easy_q_ids = '', 0, (CHAR_LENGTH(vs.easy_q_ids) - CHAR_LENGTH(REPLACE(vs.easy_q_ids, ',', '')) + 1)) +
               IF(vs.medium_q_ids IS NULL OR vs.medium_q_ids = '', 0, (CHAR_LENGTH(vs.medium_q_ids) - CHAR_LENGTH(REPLACE(vs.medium_q_ids, ',', '')) + 1)) +
               IF(vs.hard_q_ids IS NULL OR vs.hard_q_ids = '', 0, (CHAR_LENGTH(vs.hard_q_ids) - CHAR_LENGTH(REPLACE(vs.hard_q_ids, ',', '')) + 1))
            ) as total_questions,
            
            -- Dynamic Max Score
            (
               (IF(vs.easy_q_ids IS NULL OR vs.easy_q_ids = '', 0, (CHAR_LENGTH(vs.easy_q_ids) - CHAR_LENGTH(REPLACE(vs.easy_q_ids, ',', '')) + 1)) * vc.easy_marks) +
               (IF(vs.medium_q_ids IS NULL OR vs.medium_q_ids = '', 0, (CHAR_LENGTH(vs.medium_q_ids) - CHAR_LENGTH(REPLACE(vs.medium_q_ids, ',', '')) + 1)) * vc.medium_marks) +
               (IF(vs.hard_q_ids IS NULL OR vs.hard_q_ids = '', 0, (CHAR_LENGTH(vs.hard_q_ids) - CHAR_LENGTH(REPLACE(vs.hard_q_ids, ',', '')) + 1)) * vc.hard_marks)
            ) as max_score,
            
            CAST(COALESCE(vr.total_score, 0) AS UNSIGNED) AS score,
            
            -- Recalculate Percentage
            ROUND((COALESCE(vr.total_score, 0) / 
                GREATEST(
                   (IF(vs.easy_q_ids IS NULL OR vs.easy_q_ids = '', 0, (CHAR_LENGTH(vs.easy_q_ids) - CHAR_LENGTH(REPLACE(vs.easy_q_ids, ',', '')) + 1)) * vc.easy_marks) +
                   (IF(vs.medium_q_ids IS NULL OR vs.medium_q_ids = '', 0, (CHAR_LENGTH(vs.medium_q_ids) - CHAR_LENGTH(REPLACE(vs.medium_q_ids, ',', '')) + 1)) * vc.medium_marks) +
                   (IF(vs.hard_q_ids IS NULL OR vs.hard_q_ids = '', 0, (CHAR_LENGTH(vs.hard_q_ids) - CHAR_LENGTH(REPLACE(vs.hard_q_ids, ',', '')) + 1)) * vc.hard_marks)
                , 1)
            ) * 100, 2) AS percentage,
            
            CASE 
                WHEN vs.started_at IS NOT NULL THEN DATE_FORMAT(vs.started_at, '%Y-%m-%d %H:%i:%S')
                ELSE 'N/A'
            END as created_at
            
        FROM viva_sessions vs
        JOIN users u ON vs.student_id = u.id
        JOIN subjects sub ON vs.subject_id = sub.id
        JOIN viva_config vc ON sub.id = vc.subject_id
        LEFT JOIN viva_reports vr ON vs.id = vr.session_id
        WHERE vs.is_submitted = TRUE 
        ORDER BY vs.started_at DESC
        """
    )
    
    reports = cursor.fetchall()
    
    cursor.close()
    conn.close()
            
    return jsonify(reports), 200
