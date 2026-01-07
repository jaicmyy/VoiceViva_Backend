from flask import Blueprint, request, jsonify
import pymysql
from datetime import datetime

student_assignment_bp = Blueprint(
    "student_assignment",
    __name__,
    url_prefix="/api/admin/student-assignments"
)

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

# --------------------------------------------------
# ASSIGN SUBJECT TO STUDENT
# --------------------------------------------------
@student_assignment_bp.route("", methods=["POST"])
def assign_student():
    data = request.get_json(silent=True) or {}

    registration_number = data.get("registration_number")
    subject_id = data.get("subject_id")
    password = data.get("password")

    if not registration_number or not subject_id or not password:
        return jsonify({"error": "registration_number, subject_id and password are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ ENSURE SCHEMA IS CORRECT (Migration on the fly)
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                registration_number VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'student') DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"[MIGRATION ERROR] {e}")

    try:
        # --------------------------------------------------
        # 1️⃣ CREATE OR UPDATE USER
        # --------------------------------------------------
        cursor.execute(
            "SELECT id FROM users WHERE registration_number = %s",
            (registration_number,)
        )
        user = cursor.fetchone()

        if user:
            student_id = user["id"]
            cursor.execute(
                "UPDATE users SET password = %s WHERE id = %s",
                (password, student_id)
            )
        else:
            cursor.execute(
                """
                INSERT INTO users (name, registration_number, password, role)
                VALUES (%s, %s, %s, 'student')
                """,
                (registration_number, registration_number, password)
            )
            student_id = cursor.lastrowid

        # --------------------------------------------------
        # 2️⃣ PREVENT DUPLICATE ASSIGNMENT
        # --------------------------------------------------
        cursor.execute(
            """
            SELECT id FROM student_assignments
            WHERE student_id = %s AND subject_id = %s
            """,
            (student_id, subject_id)
        )
        if cursor.fetchone():
            conn.rollback()
            return jsonify({"error": "Subject already assigned to this student"}), 409

        # --------------------------------------------------
        # 3️⃣ ASSIGN SUBJECT
        # --------------------------------------------------
        cursor.execute(
            """
            INSERT INTO student_assignments (student_id, subject_id, assigned_at)
            VALUES (%s, %s, %s)
            """,
            (student_id, subject_id, datetime.now())
        )

        conn.commit()

        return jsonify({
            "message": "Student assigned successfully",
            "student_id": student_id,
            "subject_id": subject_id,
            "plain_password": password
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({
            "error": "Failed to assign student",
            "details": str(e)
        }), 500

    finally:
        cursor.close()
        conn.close()

# --------------------------------------------------
# GET ALL STUDENT ASSIGNMENTS (ADMIN VIEW)
# --------------------------------------------------
@student_assignment_bp.route("", methods=["GET"])
def get_assignments():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            sa.id,
            u.registration_number,
            s.name AS subject_name,
            u.password AS plain_password,
            sa.assigned_at
        FROM student_assignments sa
        JOIN users u ON sa.student_id = u.id
        JOIN subjects s ON sa.subject_id = s.id
        ORDER BY sa.assigned_at DESC
        """
    )

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify(rows), 200
