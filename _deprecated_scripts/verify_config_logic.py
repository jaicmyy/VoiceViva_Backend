
import pymysql
import os
import time

# --- SETUP ---
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "voice_viva_db",
    "cursorclass": pymysql.cursors.DictCursor
}

def get_conn():
    return pymysql.connect(**DB_CONFIG)

try:
    conn = get_conn()
    cursor = conn.cursor()

    # 1. SETUP DUMMY DATA
    print("Setting up test data...")
    # Create a dummy Subject (Corrected Columns)
    cursor.execute("INSERT IGNORE INTO subjects (id, name, code) VALUES (999, 'Test Subject', 'TS101')")
    
    # Create a dummy Config (Unique Marks: Easy=11, Medium=22, Hard=33)
    cursor.execute("""
        INSERT INTO viva_config 
        (subject_id, duration_minutes, total_marks, easy_marks, easy_questions, medium_marks, medium_questions, hard_marks, hard_questions) 
        VALUES (999, 10, 100, 11, 1, 22, 1, 33, 1)
        ON DUPLICATE KEY UPDATE 
        easy_marks=11, medium_marks=22, hard_marks=33
    """)

    # Create dummy Questions
    cursor.execute("INSERT IGNORE INTO questions (id, subject_id, question_text, difficulty, concepts) VALUES (9991, 999, 'What is a test?', 'easy', 'testing')")

    # Create am dummy Student (Corrected Columns, NO EMAIL)
    cursor.execute("INSERT IGNORE INTO users (id, name, password, role, registration_number) VALUES (999, 'Test Student', 'pass', 'student', 'TEST001')")

    # Create a dummy Session
    cursor.execute("""
        INSERT INTO viva_sessions (id, student_id, subject_id, easy_q_ids, current_index, is_submitted) 
        VALUES (9999, 999, 999, '9991', 0, 0)
        ON DUPLICATE KEY UPDATE subject_id=999
    """)
    conn.commit()

    # 2. RUN TEST: Simulate Route Logic (PARTIAL)
    print("Verifying Config Retrieval Logic...")
    session_id = 9999
    
    cursor.execute(
        """
        SELECT easy_marks, medium_marks, hard_marks 
        FROM viva_config 
        WHERE subject_id = (SELECT subject_id FROM viva_sessions WHERE id=%s)
        """,
        (session_id,)
    )
    config = cursor.fetchone()
    
    print(f"   Fetched Config: {config}")
    
    if config['easy_marks'] == 11 and config['medium_marks'] == 22:
        print("SUCCESS: Correctly fetched dynamic marks from DB!")
    else:
        print("FAILURE: Did not fetch expected marks (11, 22, 33).")

    # 3. CLEANUP
    print("Cleaning up...")
    cursor.execute("DELETE FROM viva_sessions WHERE id=9999")
    cursor.execute("DELETE FROM viva_config WHERE subject_id=999")
    cursor.execute("DELETE FROM questions WHERE subject_id=999")
    cursor.execute("DELETE FROM subjects WHERE id=999")
    cursor.execute("DELETE FROM users WHERE id=999")
    conn.commit()

except Exception as e:
    print(f"ERROR: {e}")
finally:
    if 'conn' in locals(): conn.close()
