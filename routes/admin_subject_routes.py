import os
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
# ADD SUBJECT (WITH PDF UPLOAD)
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

    # Save PDF
    filename = secure_filename(file.filename)
    save_path = os.path.join(
        current_app.config["SYLLABUS_FOLDER"], filename
    )
    file.save(save_path)
    pdf_path = save_path  # ✅ DEFINE IT

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO subjects (name, code, syllabus_pdf)
            VALUES (%s, %s, %s)
            """,
            (name, code, filename)
        )
        conn.commit()
        subject_id = cursor.lastrowid

    except pymysql.err.IntegrityError:
        return jsonify({"error": "Subject code already exists"}), 409

    finally:
        cursor.close()
        conn.close()

    # Generate questions (sync, safe)
    try:
        generate_and_store_questions(subject_id, name, pdf_path)
    except Exception as e:
        return jsonify({
            "error": "Subject added but question generation failed",
            "details": str(e)
        }), 500

    return jsonify({
        "message": "Subject added successfully",
        "subject_id": subject_id
    }), 201


# ------------------------------------
# GET ALL SUBJECTS
# ------------------------------------
@admin_subject_bp.route("", methods=["GET"])
def get_subjects():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM subjects")
    subjects = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(subjects), 200


# ------------------------------------
# UPDATE SUBJECT
# ------------------------------------
@admin_subject_bp.route("/<int:subject_id>", methods=["PUT"])
def update_subject(subject_id):
    name = request.form.get("name")
    code = request.form.get("code")
    file = request.files.get("syllabus")

    conn = get_db_connection()
    cursor = conn.cursor()

    if file:
        if not allowed_file(file.filename):
            return jsonify({"error": "Only PDF files allowed"}), 400

        filename = secure_filename(file.filename)
        save_path = os.path.join(
            current_app.config["SYLLABUS_FOLDER"], filename
        )
        file.save(save_path)
        pdf_path = save_path

        cursor.execute(
            """
            UPDATE subjects
            SET name=%s, code=%s, syllabus_pdf=%s
            WHERE id=%s
            """,
            (name, code, filename, subject_id)
        )

        conn.commit()

        # regenerate questions
        generate_and_store_questions(subject_id, name, pdf_path)

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

    cursor.close()
    conn.close()

    return jsonify({"message": "Subject updated successfully"}), 200


# ------------------------------------
# DELETE SUBJECT
# ------------------------------------
@admin_subject_bp.route("/<int:subject_id>", methods=["DELETE"])
def delete_subject(subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM subjects WHERE id=%s",
        (subject_id,)
    )
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "Subject deleted successfully"}), 200


# ------------------------------------
# MANUAL QUESTION GENERATION
# ------------------------------------
@admin_subject_bp.route("/<int:subject_id>/generate-questions", methods=["POST"])
def generate_questions(subject_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name, syllabus_pdf FROM subjects WHERE id=%s",
        (subject_id,)
    )
    subject = cursor.fetchone()

    cursor.close()
    conn.close()

    if not subject:
        return jsonify({"error": "Subject not found"}), 404

    pdf_path = os.path.join(
        current_app.config["SYLLABUS_FOLDER"],
        subject["syllabus_pdf"]
    )

    generate_and_store_questions(
        subject_id,
        subject["name"],
        pdf_path
    )

    return jsonify({"message": "Questions generated successfully"}), 200
