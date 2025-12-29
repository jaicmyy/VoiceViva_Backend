from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime

student_assign_bp = Blueprint(
    "student_assign",
    __name__,
    url_prefix="/api/admin/assignments"
)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# ------------------------------------
# ASSIGN SUBJECT TO STUDENT
# ------------------------------------
@student_assign_bp.route("", methods=["POST"])
def assign_subject():
    data = request.json or {}

    student_id = data.get("student_id")
    subject_id = data.get("subject_id")

    if not student_id or not subject_id:
        return jsonify({"error": "student_id and subject_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # prevent duplicate assignment
    cursor.execute(
        """
        SELECT id FROM student_assignments
        WHERE student_id=%s AND subject_id=%s
        """,
        (student_id, subject_id)
    )
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Already assigned"}), 200

    cursor.execute(
        """
        INSERT INTO student_assignments
        (student_id, subject_id, assigned_at)
        VALUES (%s, %s, %s)
        """,
        (student_id, subject_id, datetime.now())
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Subject assigned successfully"}), 201
