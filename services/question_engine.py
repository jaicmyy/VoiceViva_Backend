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

    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    # DEFAULT VALUES (🔥 IMPORTANT)
    easy_ids = []
    medium_ids = []
    hard_ids = []

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
        cursor.close()
        conn.close()
        return easy_ids, medium_ids, hard_ids   # ✅ SAFE RETURN

    # Counts
    easy_count = config["easy_questions"]
    medium_count = config["medium_questions"]
    hard_count = config["hard_questions"]

    # EASY
    cursor.execute(
        """
        SELECT id FROM questions
        WHERE subject_id=%s AND difficulty='easy'
        ORDER BY RAND()
        LIMIT %s
        """,
        (subject_id, easy_count)
    )
    easy_ids = [r["id"] for r in cursor.fetchall()]

    # MEDIUM
    cursor.execute(
        """
        SELECT id FROM questions
        WHERE subject_id=%s AND difficulty='medium'
        ORDER BY RAND()
        LIMIT %s
        """,
        (subject_id, medium_count)
    )
    medium_ids = [r["id"] for r in cursor.fetchall()]

    # HARD
    cursor.execute(
        """
        SELECT id FROM questions
        WHERE subject_id=%s AND difficulty='hard'
        ORDER BY RAND()
        LIMIT %s
        """,
        (subject_id, hard_count)
    )
    hard_ids = [r["id"] for r in cursor.fetchall()]

    cursor.close()
    conn.close()

    return easy_ids, medium_ids, hard_ids
