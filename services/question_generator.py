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
    print(f"Background question generation started for {subject_name} (ID: {subject_id})")
    import random

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 0 Fetch marks configuration (Updated comment)
        cursor.execute(
            "SELECT easy_questions, medium_questions, hard_questions FROM viva_config WHERE subject_id = %s",
            (subject_id,)
        )
        config = cursor.fetchone()
        
        # Default fallback if no config found yet
        if config:
            REQUIRED_COUNTS = {
                "easy": config["easy_questions"],
                "medium": config["medium_questions"],
                "hard": config["hard_questions"]
            }
        else:
            REQUIRED_COUNTS = {"easy": 5, "medium": 5, "hard": 5}

        # Update status to pending
        cursor.execute("UPDATE subjects SET generation_status='pending' WHERE id=%s", (subject_id,))
        conn.commit()

        # 1 Extract text
        text = extract_text_from_pdf(syllabus_pdf_path)

        # 2 Extract MORE concepts (increased limit)
        concepts = extract_concepts(text, max_concepts=100)
        
        if not concepts:
            print("No concepts extracted. Aborting generation.")
            raise Exception("No concepts extracted from PDF")

        inserted = 0
        print(f"Extracted {len(concepts)} concepts from {syllabus_pdf_path}...")

        # 3 GENERATION LOOP
        for difficulty in ["easy", "medium", "hard"]:
            needed = REQUIRED_COUNTS[difficulty]
            
            # Check how many we already have (in case of partial run)
            cursor.execute(
                "SELECT COUNT(*) as cnt FROM questions WHERE subject_id=%s AND difficulty=%s",
                (subject_id, difficulty)
            )
            current_count = cursor.fetchone()["cnt"]
            
            if current_count >= needed:
                print(f"Already have {current_count}/{needed} {difficulty} questions. Skipping.")
                continue

            to_generate = needed - current_count
            print(f"Generating {to_generate} more [{difficulty}] questions (Total needed: {needed})...")
            
            attempts = 0
            max_attempts = to_generate * 5  # Safety break
            
            # Loop until we have enough questions
            while current_count < needed and attempts < max_attempts:
                # Shuffle concepts to avoid order bias in retries
                random.shuffle(concepts)
                
                for item in concepts:
                    if current_count >= needed:
                        break
                        
                    attempts += 1
                    concept = item["concept"]
                    context = item["context"]
                    
                    try:
                        # Extract context-aware question
                        q = generate_single_question(
                            subject_name,
                            concept,
                            context,
                            difficulty
                        )
                        if not q:
                            continue

                        # Dedup check (using question_text column)
                        cursor.execute(
                            "SELECT COUNT(*) AS cnt FROM questions WHERE subject_id=%s AND question_text=%s",
                            (subject_id, q["question"])
                        )

                        if cursor.fetchone()["cnt"] > 0:
                            print(f"Duplicate question skipped: {q['question'][:30]}...")
                            continue

                        cursor.execute(
                            """
                            INSERT INTO questions (subject_id, difficulty, question_text, concepts)
                            VALUES (%s, %s, %s, %s)
                            """,
                            (subject_id, q["difficulty"], q["question"], concept)
                        )

                        conn.commit()
                        current_count += 1
                        inserted += 1
                        print(f"[{current_count}/{needed}] Generated {difficulty} question for: {concept[:30]}...")
                    
                    except Exception as e:
                        print(f"[LLM ERROR] {difficulty} | {concept[:30]}... : {e}")

            if current_count < needed:
                print(f"WARNING: Could not generate enough {difficulty} questions. Got {current_count}/{needed}.")

        # Update status to completed
        cursor.execute("UPDATE subjects SET generation_status='completed' WHERE id=%s", (subject_id,))
        conn.commit()
        print(f"Total questions inserted this run: {inserted}. Generation completed.")
        return inserted

    except Exception as e:
        print(f"Background generation failed: {e}")
        try:
            cursor.execute("UPDATE subjects SET generation_status='failed' WHERE id=%s", (subject_id,))
            conn.commit()
        except: pass
        return 0
    finally:
        cursor.close()
        conn.close()
