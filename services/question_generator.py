import pymysql

from services.llm_client import generate_single_question
from services.pdf_parser import extract_text_from_pdf
from services.concept_extractor import extract_concepts


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )


def generate_and_store_questions(subject_id, subject_name, syllabus_pdf_path):
    print("🧵 Background question generation started")

    # 1️⃣ Extract text
    text = extract_text_from_pdf(syllabus_pdf_path)

    # 2️⃣ Extract MORE concepts (this is the key)
    concepts = extract_concepts(text, max_concepts=30)

    conn = get_db_connection()
    cursor = conn.cursor()

    inserted = 0
    

    for concept in concepts:
        for difficulty in ["easy", "medium", "hard"]:
            try:
                # 🔹 ONE concept per call (FAST + SAFE)
                q = generate_single_question(
                    subject_name,
                    [concept],
                    difficulty
                )
                if not q:
                    continue

                # 🔒 Dedup check
                cursor.execute(
                    """
                    SELECT COUNT(*) AS cnt FROM questions
                    WHERE subject_id=%s AND question_text=%s
                    """,
                    (subject_id, q["question"])
                )

                if cursor.fetchone()["cnt"] > 0:
                    continue

                cursor.execute(
                    """
                    INSERT INTO questions (subject_id, difficulty, question_text)
                    VALUES (%s, %s, %s)
                    """,
                    (subject_id, q["difficulty"], q["question"])
                )

                conn.commit()
                inserted += 1
                print(f"✅ Inserted [{difficulty}] → {concept}")

            except Exception as e:
                print(f"[LLM ERROR] {difficulty} | {concept[:40]}... : {e}")
            if len(concept.split()) > 12:
                continue

                

    cursor.close()
    conn.close()

    print(f"🎉 Total questions inserted: {inserted}")
    return inserted
