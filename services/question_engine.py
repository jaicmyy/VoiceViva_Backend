import pymysql

# Difficulty → Marks mapping
DIFFICULTY_MARKS = {
    "easy": 2,
    "medium": 5,
    "hard": 10
}


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )



def select_questions_for_viva(subject_id):
    import pymysql
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # DEFAULT VALUES
    easy_ids = []
    medium_ids = []
    hard_ids = []

    try:
        # 1️⃣ Fetch viva config
        cursor.execute(
            """
            SELECT easy_questions, medium_questions, hard_questions
            FROM viva_config
            WHERE subject_id = %s
            """,
            (subject_id,)
        )
        config = cursor.fetchone()

        if not config:
            logger.warning(f"No viva config found for subject_id={subject_id}")
            return easy_ids, medium_ids, hard_ids

        # Counts from config
        easy_count = int(config.get("easy_questions") or 0)
        medium_count = int(config.get("medium_questions") or 0)
        hard_count = int(config.get("hard_questions") or 0)

        logger.info(f"Viva config for subject {subject_id}: Easy={easy_count}, Medium={medium_count}, Hard={hard_count}")

        # Helper to fetch questions
        def fetch_questions(difficulty, count):
            if count <= 0: return []
            cursor.execute(
                """
                SELECT id FROM questions
                WHERE subject_id=%s AND difficulty=%s
                ORDER BY RAND()
                LIMIT %s
                """,
                (subject_id, difficulty, count)
            )
            return [r["id"] for r in cursor.fetchall()]

        # Select questions
        easy_ids = fetch_questions("easy", easy_count)
        medium_ids = fetch_questions("medium", medium_count)
        hard_ids = fetch_questions("hard", hard_count)
        
        # Log validation
        if len(easy_ids) < easy_count:
            logger.warning(f"Wanted {easy_count} easy, got {len(easy_ids)}")
        if len(medium_ids) < medium_count:
            logger.warning(f"Wanted {medium_count} medium, got {len(medium_ids)}")
        if len(hard_ids) < hard_count:
            logger.warning(f"Wanted {hard_count} hard, got {len(hard_ids)}")

    except Exception as e:
        logger.error(f"Error selecting questions: {e}")
    finally:
        cursor.close()
        conn.close()

    logger.info(f"Selected questions - Easy: {len(easy_ids)}, Medium: {len(medium_ids)}, Hard: {len(hard_ids)}")

    return easy_ids, medium_ids, hard_ids

