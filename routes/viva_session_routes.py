from flask import Blueprint, request, jsonify, session
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
from flask import Blueprint, request, jsonify, session
import pymysql

from services.question_engine import select_questions_for_viva

@viva_session_bp.route("/start", methods=["POST"])
def start_viva():
    data = request.json or {}

    # ✅ GET STUDENT FROM SESSION
    student_id = session.get("user_id")
    subject_id = data.get("subject_id")

    if not student_id:
        return jsonify({"error": "User not logged in"}), 401

    if not subject_id:
        return jsonify({"error": "subject_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # -------------------------------
    # GET VIVA CONFIGURATION
    # -------------------------------
    cursor.execute(
        """
        SELECT duration_minutes
        FROM viva_config
        WHERE subject_id = %s
        """,
        (subject_id,)
    )
    config = cursor.fetchone()

    if not config:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Viva configuration not found for this subject"
        }), 400

    duration_minutes = config["duration_minutes"]

    # -------------------------------
    # SELECT QUESTIONS (CONFIG-BASED)
    # -------------------------------
    result = select_questions_for_viva(subject_id)

    # 🛡️ SAFETY CHECK
    if not result or len(result) != 3:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "Invalid viva configuration or question selection failed"
        }), 400

    easy_ids, medium_ids, hard_ids = result

    if not easy_ids and not medium_ids and not hard_ids:
        cursor.close()
        conn.close()
        return jsonify({
            "error": "No questions available as per viva configuration"
        }), 400

    question_ids = easy_ids + medium_ids + hard_ids

    # -------------------------------
    # CREATE VIVA SESSION
    # -------------------------------
    cursor.execute(
        """
        INSERT INTO viva_sessions (student_id, subject_id, current_index)
        VALUES (%s, %s, 0)
        """,
        (student_id, subject_id)
    )
    session_id = cursor.lastrowid

    # -------------------------------
    # FETCH QUESTION TEXT (ORDER SAFE)
    # -------------------------------
    format_ids = ",".join(["%s"] * len(question_ids))
    cursor.execute(
        f"""
        SELECT id, question_text
        FROM questions
        WHERE id IN ({format_ids})
        """,
        tuple(question_ids)
    )
    rows = cursor.fetchall()

    question_map = {q["id"]: q["question_text"] for q in rows}

    ordered_questions = [
        {"id": qid, "text": question_map[qid]}
        for qid in question_ids
        if qid in question_map
    ]

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "session_id": session_id,
        "questions": ordered_questions,
        "total_questions": len(ordered_questions),
        "duration_minutes": duration_minutes
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

    # -------------------------------
    # SAVE AUDIO
    # -------------------------------
    os.makedirs("uploads/audio_answers", exist_ok=True)
    filename = f"{session_id}_{question_id}.webm"
    path = os.path.join("uploads/audio_answers", filename)
    audio.save(path)

    # -------------------------------
    # TRANSCRIBE AUDIO
    # -------------------------------
    transcript = transcribe_audio(path)

    # -------------------------------
    # FETCH QUESTION DIFFICULTY
    # -------------------------------
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

    # -------------------------------
    # EVALUATE ANSWER
    # -------------------------------
    score = evaluate_answer(transcript, max_marks)

    # -------------------------------
    # STORE ANSWER
    # -------------------------------
    cursor.execute(
        """
        INSERT INTO viva_answers
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
