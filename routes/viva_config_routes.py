from flask import Blueprint, request, jsonify
import pymysql

viva_config_bp = Blueprint(
    "viva_config",
    __name__,
    url_prefix="/api/admin/viva-config"
)


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )


@viva_config_bp.route("", methods=["POST"])
def save_viva_config():
    data = request.json

    subject_id = data.get("subject_id")
    duration = data.get("duration_minutes")
    total_marks = data.get("total_marks")

    easy_marks = data.get("easy_marks", 0)
    medium_marks = data.get("medium_marks", 0)
    hard_marks = data.get("hard_marks", 0)

    if not subject_id or not duration or not total_marks:
        return jsonify({"error": "Missing required fields"}), 400

    # ---- AUTO CALCULATION (STRICT) ----
    easy_q = easy_marks // 2
    medium_q = medium_marks // 5
    hard_q = hard_marks // 8

    conn = get_db_connection()
    cursor = conn.cursor()

    # Remove old config if exists
    cursor.execute(
        "DELETE FROM viva_config WHERE subject_id=%s",
        (subject_id,)
    )

    cursor.execute(
        """
        INSERT INTO viva_config (
            subject_id,
            duration_minutes,
            total_marks,
            easy_marks, easy_questions,
            medium_marks, medium_questions,
            hard_marks, hard_questions
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            subject_id,
            duration,
            total_marks,
            easy_marks, easy_q,
            medium_marks, medium_q,
            hard_marks, hard_q
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Viva configuration saved",
        "summary": {
            "easy": {"marks": easy_marks, "questions": easy_q},
            "medium": {"marks": medium_marks, "questions": medium_q},
            "hard": {"marks": hard_marks, "questions": hard_q},
            "total_questions": easy_q + medium_q + hard_q,
            "total_marks": total_marks,
            "duration_minutes": duration
        }
    }), 201
