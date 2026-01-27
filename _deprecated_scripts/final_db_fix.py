import pymysql
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def sync_schema():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        logger.info("Starting Final Schema Sync...")

        # 1. Subjects Table
        logger.info("Checking 'subjects' table...")
        cursor.execute("SHOW COLUMNS FROM subjects LIKE 'generation_status'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE subjects ADD COLUMN generation_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending'")
            logger.info("Added 'generation_status' to 'subjects'")

        # 2. Questions Table
        logger.info("Checking 'questions' table...")
        cursor.execute("SHOW COLUMNS FROM questions LIKE 'question_text'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE questions CHANGE COLUMN question question_text TEXT")
            logger.info("Renamed 'question' to 'question_text' in 'questions'")
        
        cursor.execute("SHOW COLUMNS FROM questions LIKE 'concepts'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE questions ADD COLUMN concepts TEXT AFTER question_text")
            logger.info("Added 'concepts' to 'questions'")

        # 3. Viva Answers Table
        logger.info("Checking 'viva_answers' table...")
        cursor.execute("SHOW COLUMNS FROM viva_answers LIKE 'feedback'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE viva_answers ADD COLUMN feedback TEXT AFTER max_score")
            logger.info("Added 'feedback' to 'viva_answers'")

        cursor.execute("SHOW COLUMNS FROM viva_answers LIKE 'confidence'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE viva_answers ADD COLUMN confidence FLOAT AFTER feedback")
            logger.info("Added 'confidence' to 'viva_answers'")

        cursor.execute("SHOW COLUMNS FROM viva_answers LIKE 'evaluation_method'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE viva_answers ADD COLUMN evaluation_method VARCHAR(50) DEFAULT 'llm'")
            logger.info("Added 'evaluation_method' to 'viva_answers'")

        # Add Unique constraint to prevent duplicate answers for same question in a session
        try:
            cursor.execute("ALTER TABLE viva_answers ADD UNIQUE INDEX uniq_session_q (session_id, question_id)")
            logger.info("Added unique index to 'viva_answers'")
        except Exception:
            logger.info("Unique index on 'viva_answers' already exists")

        # 4. Viva Sessions Table
        logger.info("Checking 'viva_sessions' table...")
        cursor.execute("SHOW COLUMNS FROM viva_sessions LIKE 'is_submitted'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE viva_sessions ADD COLUMN is_submitted BOOLEAN DEFAULT FALSE")
            logger.info("Added 'is_submitted' to 'viva_sessions'")

        cursor.execute("SHOW COLUMNS FROM viva_sessions LIKE 'submitted_at'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE viva_sessions ADD COLUMN submitted_at DATETIME")
            logger.info("Added 'submitted_at' to 'viva_sessions'")

        # 5. Viva Reports Table
        logger.info("Checking 'viva_reports' table...")
        cursor.execute("SHOW COLUMNS FROM viva_reports LIKE 'pdf_path'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE viva_reports ADD COLUMN pdf_path VARCHAR(255) AFTER grade")
            logger.info("Added 'pdf_path' to 'viva_reports'")

        # Ensure total_questions, total_score, etc. exist
        cols_to_add = {
            'total_questions': 'INT',
            'total_score': 'FLOAT',
            'max_total_score': 'FLOAT',
            'percentage': 'FLOAT',
            'grade': 'VARCHAR(5)'
        }
        for col, col_type in cols_to_add.items():
            cursor.execute(f"SHOW COLUMNS FROM viva_reports LIKE '{col}'")
            if not cursor.fetchone():
                cursor.execute(f"ALTER TABLE viva_reports ADD COLUMN {col} {col_type}")
                logger.info(f"Added '{col}' to 'viva_reports'")

        conn.commit()
        logger.info("✅ Schema sync completed successfully!")

    except Exception as e:
        conn.rollback()
        logger.error(f"❌ Schema sync failed: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    sync_schema()
