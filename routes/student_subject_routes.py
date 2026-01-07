from flask import Blueprint, jsonify, session
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
    registration_number = session.get("registration_number")

    if not registration_number:
        return jsonify({"error": "Unauthorized"}), 401

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
        LIMIT 1
        """,
        (registration_number,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()

    if not row:
        return jsonify({"error": "No subject assigned"}), 404

    return jsonify({
        "registration_number": row["registration_number"],
        "subject_id": row["subject_id"],
        "subject_name": row["subject_name"]
    }), 200
