from flask import Blueprint, jsonify, session, request
import pymysql

student_subject_bp = Blueprint(
    "student_subject",
    __name__,
    url_prefix="/api/student"
)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# --------------------------------------------------
# GET ASSIGNED SUBJECT FOR LOGGED-IN STUDENT
# --------------------------------------------------
@student_subject_bp.route("/assigned-subject", methods=["GET"])
def get_assigned_subject():
    # Attempt to get from session, then from custom header
    registration_number = session.get("registration_number") or request.headers.get("X-Registration-Number")

    if not registration_number:
        return jsonify({"error": "Unauthorized: Registration number not found"}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            sa.subject_id,
            sub.name AS subject_name,
            u.registration_number
        FROM student_assignments sa
        JOIN users u ON sa.student_id = u.id
        JOIN subjects sub ON sa.subject_id = sub.id
        WHERE u.registration_number = %s
        """,
        (registration_number,)
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    if not rows:
        return jsonify([]), 200 # Return empty list if no subjects

    return jsonify(rows), 200
