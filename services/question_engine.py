import pymysql
# Difficulty → Marks mapping
DIFFICULTY_MARKS = {
    "easy": 2,
    "medium": 5,
    "hard": 7
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
    """
    Select questions based on viva_config for a subject.
    Returns question metadata with marks.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM viva_config WHERE subject_id=%s",
        (subject_id,)
    )
    config = cursor.fetchone()

    if not config:
        cursor.close()
        conn.close()
        raise Exception("Viva configuration not found")

    def fetch_questions(level, count):
        cursor.execute(
            """
            SELECT id, question_text FROM questions
            WHERE subject_id=%s AND difficulty=%s
            ORDER BY RAND()
            LIMIT %s
            """,
            (subject_id, level, count)
        )

        return [
            {
                "question_id": row["id"],
                "question_text": row["question_text"],
                "difficulty": level,
                "max_marks": DIFFICULTY_MARKS[level]
            }
            for row in cursor.fetchall()
        ]

    easy_qs = fetch_questions("easy", config["easy_questions"])
    medium_qs = fetch_questions("medium", config["medium_questions"])
    hard_qs = fetch_questions("hard", config["hard_questions"])

    if (
        len(easy_qs) < config["easy_questions"]
        or len(medium_qs) < config["medium_questions"]
        or len(hard_qs) < config["hard_questions"]
    ):
        cursor.close()
        conn.close()
        raise Exception("Insufficient questions in database")

    cursor.close()
    conn.close()

    return easy_qs + medium_qs + hard_qs
def calculate_total_viva_marks(questions):
    return sum(q["max_marks"] for q in questions)
