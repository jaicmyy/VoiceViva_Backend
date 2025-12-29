from flask import Blueprint, request, jsonify
import pymysql
import os

from services.question_engine import select_questions_for_viva
from services.speech_to_text import transcribe_audio
from services.answer_evaluator import evaluate_answer

viva_session_bp = Blueprint(
    "viva_session",
    __name__,
    url_prefix="/api/viva"
)


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )


# ----------------------------------
# START VIVA SESSION
# ----------------------------------
@viva_session_bp.route("/start", methods=["POST"])
def start_viva():
    data = request.json or {}

    student_id = data.get("student_id")
    subject_id = data.get("subject_id")

    if not student_id or not subject_id:
        return jsonify({"error": "student_id and subject_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # ❗ Check existing session
    cursor.execute(
        """
        SELECT id FROM viva_sessions
        WHERE student_id=%s AND subject_id=%s
        """,
        (student_id, subject_id)
    )
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"message": "Viva already started"}), 200

    # ✅ Select questions BASED ON VIVA CONFIG
    try:
        easy_ids, medium_ids, hard_ids = select_questions_for_viva(subject_id)
    except Exception as e:
        cursor.close()
        conn.close()
        return jsonify({"error": str(e)}), 500

    # Convert IDs safely to CSV
    easy_csv = ",".join(str(q) for q in easy_ids)
    medium_csv = ",".join(str(q) for q in medium_ids)
    hard_csv = ",".join(str(q) for q in hard_ids)

    # ✅ Insert viva session
    cursor.execute(
        """
        INSERT INTO viva_sessions (
            student_id,
            subject_id,
            easy_q_ids,
            medium_q_ids,
            hard_q_ids,
            current_index
        )
        VALUES (%s,%s,%s,%s,%s,%s)
        """,
        (
            student_id,
            subject_id,
            easy_csv,
            medium_csv,
            hard_csv,
            0
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "message": "Viva started successfully",
        "easy_questions": len(easy_ids),
        "medium_questions": len(medium_ids),
        "hard_questions": len(hard_ids)
    }), 201


# ----------------------------------
# SUBMIT ANSWER (AUDIO → STT → SCORE)
# ----------------------------------
@viva_session_bp.route("/<int:session_id>/answer", methods=["POST"])
def submit_answer(session_id):
    audio = request.files.get("audio")
    question_id = request.form.get("question_id")

    if not audio or not question_id:
        return jsonify({"error": "audio and question_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # Save audio
    os.makedirs("uploads/audio_answers", exist_ok=True)
    filename = f"{session_id}_{question_id}.webm"
    path = os.path.join("uploads/audio_answers", filename)
    audio.save(path)

    # ✅ Transcribe audio
    transcript = transcribe_audio(path)

    # ✅ Fetch difficulty
    cursor.execute(
        "SELECT difficulty FROM questions WHERE id=%s",
        (question_id,)
    )
    row = cursor.fetchone()
    if not row:
        cursor.close()
        conn.close()
        return jsonify({"error": "Question not found"}), 404

    difficulty = row["difficulty"]

    DIFFICULTY_MARKS = {
        "easy": 2,
        "medium": 4,
        "hard": 6
    }

    max_marks = DIFFICULTY_MARKS.get(difficulty, 2)

    # ✅ Evaluate answer
    score = evaluate_answer(transcript, max_marks)

    # ✅ Store answer
    cursor.execute(
        """
        INSERT INTO answers
        (session_id, question_id, audio_path, transcript, score, max_score)
        VALUES (%s, %s, %s, %s, %s, %s)
        """,
        (
            session_id,
            question_id,
            path,
            transcript,
            score,
            max_marks
        )
    )

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"status": "saved"}), 201
