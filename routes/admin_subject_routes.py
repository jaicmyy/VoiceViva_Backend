import os
import uuid
import threading
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
import pymysql

from services.question_generator import generate_and_store_questions

admin_subject_bp = Blueprint(
    "admin_subject",
    __name__,
    url_prefix="/api/admin/subjects"
)

ALLOWED_EXTENSIONS = {"pdf"}


# ------------------------------------
# HELPERS
# ------------------------------------
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )


# ------------------------------------
# ADD SUBJECT (UPLOAD PDF + AUTO GENERATE QUESTIONS)
# ------------------------------------
@admin_subject_bp.route("", methods=["POST"])
def add_subject():
    name = request.form.get("name")
    code = request.form.get("code")
    file = request.files.get("syllabus")

    if not name or not code or not file:
        return jsonify({"error": "All fields are required"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files allowed"}), 400

    # Ensure consistent path: uploads/syllabus
    upload_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], "syllabus")
    os.makedirs(upload_dir, exist_ok=True)

    unique_filename = secure_filename(file.filename)
    pdf_path = os.path.join(upload_dir, unique_filename)
    file.save(pdf_path)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Explicitly set generation_status to pending
        cursor.execute(
            """
            INSERT INTO subjects (name, code, syllabus_pdf, generation_status)
            VALUES (%s, %s, %s, 'pending')
            """,
            (name, code, unique_filename)
        )
        conn.commit()
        subject_id = cursor.lastrowid

    except pymysql.err.IntegrityError:
        cursor.close()
        conn.close()
        return jsonify({"error": "Subject code already exists"}), 409
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

    cursor.close()
    conn.close()

    # Start generation
    thread = threading.Thread(target=generate_and_store_questions, args=(subject_id, name, pdf_path))
    thread.start()

    from datetime import datetime
    created_at_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return jsonify({
        "id": subject_id,
        "name": name,
        "code": code,
        "syllabusFile": unique_filename,
        "generation_status": "pending",
        "created_at": created_at_str
    }), 201


# ------------------------------------
# GET ALL SUBJECTS
# ------------------------------------
@admin_subject_bp.route("", methods=["GET"])
def get_subjects():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, name, code, syllabus_pdf AS syllabusFile, generation_status, created_at
        FROM subjects
        ORDER BY created_at DESC
        """
    )
    subjects = cursor.fetchall()
    cursor.close()
    conn.close()

    for row in subjects:
        if row.get("created_at") and hasattr(row["created_at"], "strftime"):
             row["created_at"] = row["created_at"].strftime("%Y-%m-%d %H:%M:%S")
    
    return jsonify(subjects), 200


@admin_subject_bp.route("/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM subjects WHERE id=%s", (subject_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Subject deleted"}), 200
@admin_subject_bp.route("/<int:subject_id>", methods=["PUT"])
def edit_subject(subject_id):
    name = request.form.get("name")
    code = request.form.get("code")
    file = request.files.get("syllabus")

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        if file and allowed_file(file.filename):
            unique_filename = secure_filename(file.filename)
            pdf_path = os.path.join(current_app.config["SYLLABUS_FOLDER"], unique_filename)
            file.save(pdf_path)

            cursor.execute(
                """
                UPDATE subjects
                SET name=%s, code=%s, syllabus_pdf=%s
                WHERE id=%s
                """,
                (name, code, unique_filename, subject_id)
            )
        else:
            cursor.execute(
                """
                UPDATE subjects
                SET name=%s, code=%s
                WHERE id=%s
                """,
                (name, code, subject_id)
            )
        
        conn.commit()
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

    return jsonify({
        "id": subject_id,
        "name": name,
        "code": code,
        "status": "updated"
    }), 200
