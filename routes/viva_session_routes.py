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


@viva_session_bp.route("/start", methods=["POST"])
def start_viva():
    data = request.json or {}
    subject_id = data.get("subject_id")

    # ✅ GET STUDENT FROM SESSION OR HEADER
    student_id = session.get("user_id")
    reg_no = request.headers.get("X-Registration-Number")

    conn = get_db_connection()
    cursor = conn.cursor()

    if not student_id and reg_no:
        cursor.execute("SELECT id FROM users WHERE registration_number = %s", (reg_no,))
        user_row = cursor.fetchone()
        if user_row:
            student_id = user_row["id"]

    if not student_id:
        cursor.close()
        conn.close()
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

    # SAFETY CHECK
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
    # Store question IDs as comma-separated strings for tracking
    easy_ids_str = ",".join(map(str, easy_ids)) if easy_ids else ""
    medium_ids_str = ",".join(map(str, medium_ids)) if medium_ids else ""
    hard_ids_str = ",".join(map(str, hard_ids)) if hard_ids else ""
    
    cursor.execute(
        """
        INSERT INTO viva_sessions (student_id, subject_id, easy_q_ids, medium_q_ids, hard_q_ids, current_index)
        VALUES (%s, %s, %s, %s, %s, 0)
        """,
        (student_id, subject_id, easy_ids_str, medium_ids_str, hard_ids_str)
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
# ----------------------------------
# SUBMIT ANSWER (ASYNC BACKGROUND)
# ----------------------------------
from services.llm_answer_evaluator import evaluate_answer_llm
from services.confidence_analyzer import calculate_confidence
import threading

def process_answer_background(session_id, question_id, audio_path, max_marks, question_text, concepts):
    """
    Background worker to process audio, transcribe, score, and update DB.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print(f"[BG] Processing answer for Session {session_id} Question {question_id}...")
        
        # 1. Transcribe
        transcript = transcribe_audio(audio_path)
        
        # 2. Evaluate
        score, feedback = evaluate_answer_llm(transcript, question_text, concepts, max_marks)
        confidence = calculate_confidence(audio_path)
        
        # 3. Update DB
        cursor.execute(
            """
            UPDATE viva_answers
            SET transcript=%s, score=%s, feedback=%s, confidence=%s, status='completed'
            WHERE session_id=%s AND question_id=%s
            """,
            (transcript, score, feedback, confidence, session_id, question_id)
        )
        conn.commit()
        print(f"[BG] Answer saved: Score {score}/{max_marks}")

    except Exception as e:
        print(f"[BG] Error processing answer: {e}")
        cursor.execute(
            "UPDATE viva_answers SET feedback=%s, status='failed', score=0 WHERE session_id=%s AND question_id=%s",
            (f"Processing Error: {str(e)}", session_id, question_id)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


@viva_session_bp.route("/<int:session_id>/answer", methods=["POST"])
def submit_answer(session_id):
    audio = request.files.get("audio")
    question_id = request.form.get("question_id")

    if not audio or not question_id:
        return jsonify({"error": "audio and question_id required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. CHECK IF QUESTION EXISTS
        cursor.execute(
            "SELECT question_text, concepts, difficulty FROM questions WHERE id=%s",
            (question_id,)
        )
        row = cursor.fetchone()
        if not row:
            return jsonify({"error": "Question not found"}), 404

        difficulty = row["difficulty"]
        question_text = row["question_text"]
        concepts = row["concepts"]

        # 1.A FETCH CONFIG MARKS
        cursor.execute(
            """
            SELECT easy_marks, medium_marks, hard_marks 
            FROM viva_config 
            WHERE subject_id = (SELECT subject_id FROM viva_sessions WHERE id=%s)
            """,
            (session_id,)
        )
        config = cursor.fetchone()
        
        # Default to old hardcoded if config missing (fallback)
        easy_marks = config["easy_marks"] if config else 2
        medium_marks = config["medium_marks"] if config else 5
        hard_marks = config["hard_marks"] if config else 10

        DIFFICULTY_MARKS = {"easy": easy_marks, "medium": medium_marks, "hard": hard_marks}
        max_marks = DIFFICULTY_MARKS.get(difficulty, easy_marks)

        # 2. SAVE FILE IMMEDIATELY
        os.makedirs("uploads/audio_answers", exist_ok=True)
        filename = f"{session_id}_{question_id}.3gp"
        path = os.path.join("uploads/audio_answers", filename)
        audio.save(path)

        # 3. INSERT PLACEHOLDER RECORD
        cursor.execute(
            """
            INSERT INTO viva_answers
            (session_id, question_id, audio_path, transcript, score, max_score, feedback, confidence, answered_at, status)
            VALUES (%s, %s, %s, '', 0, %s, 'Processing...', 0, NOW(), 'processing')
            ON DUPLICATE KEY UPDATE
                audio_path=VALUES(audio_path),
                status='processing',
                answered_at=NOW()
            """,
            (session_id, question_id, path, max_marks)
        )
        conn.commit()

        # 4. START BACKGROUND THREAD
        thread = threading.Thread(
            target=process_answer_background,
            args=(session_id, question_id, path, max_marks, question_text, concepts)
        )
        thread.start()

        # 5. RETURN SUCCESS IMMEDIATELY
        return jsonify({
            "status": "queued",
            "message": "Answer received, processing in background."
        }), 202

    except Exception as e:
        print(f"Submit Error: {e}")
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()


# ----------------------------------
# SUBMIT VIVA (FINALIZE & REPORT)
# ----------------------------------
@viva_session_bp.route("/<int:session_id>/submit", methods=["POST"])
def submit_viva(session_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 1. Fetch Session Info
        cursor.execute(
            "SELECT student_id, subject_id FROM viva_sessions WHERE id=%s",
            (session_id,)
        )
        session_info = cursor.fetchone()
        if not session_info:
            return jsonify({"error": "Session not found"}), 404

        # 2. Calculate aggregates
        cursor.execute(
            """
            SELECT 
                COUNT(*) as total_q,
                SUM(score) as total_s,
                SUM(max_score) as max_s
            FROM viva_answers
            WHERE session_id = %s
            """,
            (session_id,)
        )
        stats = cursor.fetchone()
        
        # 2.A Calculate TOTAL POSSIBLE MAX SCORE (for accurate grading)
        # Fetch session question lists and config marks
        cursor.execute(
            """
            SELECT s.easy_q_ids, s.medium_q_ids, s.hard_q_ids,
                   c.easy_marks, c.medium_marks, c.hard_marks
            FROM viva_sessions s
            JOIN viva_config c ON s.subject_id = c.subject_id
            WHERE s.id = %s
            """,
            (session_id,)
        )
        meta = cursor.fetchone()
        
        if meta:
            # Count questions
            n_easy = len(meta["easy_q_ids"].split(",")) if meta["easy_q_ids"] else 0
            n_medium = len(meta["medium_q_ids"].split(",")) if meta["medium_q_ids"] else 0
            n_hard = len(meta["hard_q_ids"].split(",")) if meta["hard_q_ids"] else 0
            
            # Use dynamic marks (fallback to defaults if config is 0/null which shouldn't happen)
            m_easy = meta["easy_marks"] or 2
            m_medium = meta["medium_marks"] or 5
            m_hard = meta["hard_marks"] or 10
            
            max_s = (n_easy * m_easy) + (n_medium * m_medium) + (n_hard * m_hard)
        else:
            # Fallback if join fails
            max_s = stats["max_s"] or 1

        total_q = stats["total_q"] or 0
        total_s = stats["total_s"] or 0
        
        # Ensure max_s is at least 1 to avoid DbZ
        max_s = max(max_s, 1)

        percentage = round((total_s / max_s) * 100, 2)
        
        # Simple Grade Logic
        if percentage >= 90: grade = "O"
        elif percentage >= 80: grade = "A+"
        elif percentage >= 70: grade = "A"
        elif percentage >= 60: grade = "B"
        else: grade = "F"

        # 3. Insert into viva_reports
        from datetime import datetime
        cursor.execute(
            """
            INSERT INTO viva_reports 
            (session_id, student_id, subject_id, total_questions, total_score, max_total_score, percentage, grade, generated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                session_id,
                session_info["student_id"],
                session_info["subject_id"],
                total_q,
                total_s,
                max_s,
                percentage,
                grade,
                datetime.now()
            )
        )

        # 4. Mark session as completed
        cursor.execute(
            "UPDATE viva_sessions SET is_submitted=TRUE, completed_at = %s WHERE id = %s",
            (datetime.now(), session_id)
        )

        conn.commit()
        return jsonify({
            "status": "completed",
            "score": total_s,
            "max_score": max_s,
            "percentage": percentage,
            "grade": grade
        }), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
