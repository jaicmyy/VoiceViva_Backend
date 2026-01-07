import os
import uuid
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

    os.makedirs(current_app.config["SYLLABUS_FOLDER"], exist_ok=True)

    # ✅ FIX: prevent filename collision
    original_filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4()}_{original_filename}"
    pdf_path = os.path.join(current_app.config["SYLLABUS_FOLDER"], unique_filename)
    file.save(pdf_path)

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO subjects (name, code, syllabus_pdf, generation_status)
            VALUES (%s, %s, %s, %s)
            """,
            (name, code, unique_filename, "pending")
        )
        conn.commit()

        subject_id = cursor.lastrowid

        # HARD VALIDATION
        cursor.execute("SELECT id FROM subjects WHERE id=%s", (subject_id,))
        if not cursor.fetchone():
            raise Exception("Subject insert failed")

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

    # --------------------------------
    # AUTO QUESTION GENERATION
    # --------------------------------
    try:
        generate_and_store_questions(subject_id, name, pdf_path)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE subjects SET generation_status=%s WHERE id=%s",
            ("completed", subject_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

    except Exception as e:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE subjects SET generation_status=%s WHERE id=%s",
            ("failed", subject_id)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({
            "error": "Subject added but question generation failed",
            "details": str(e)
        }), 500

    # ✅ CRITICAL FIX: return full subject object
    return jsonify({
        "id": str(subject_id),
        "name": name,
        "code": code,
        "syllabusFile": unique_filename,
        "generation_status": "completed"
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
        SELECT 
            id,
            name,
            code,
            syllabus_pdf AS syllabusFile,
            generation_status,
            created_at
        FROM subjects
        ORDER BY created_at DESC
        """
    )

    subjects = cursor.fetchall()
    cursor.close()
    conn.close()

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

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE subjects
        SET name=%s, code=%s
        WHERE id=%s
        """,
        (name, code, subject_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "id": subject_id,
        "name": name,
        "code": code
    }), 200
