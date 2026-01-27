import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

conn = get_db_connection()
cursor = conn.cursor()

print("--- Recent Answers (Last 5) ---")
cursor.execute("""
    SELECT id, session_id, question_id, status, score, max_score, LENGTH(transcript) as trans_len, answered_at 
    FROM viva_answers 
    ORDER BY answered_at DESC 
    LIMIT 5
""")
rows = cursor.fetchall()

if not rows:
    print("No answers found.")
else:
    for row in rows:
        print(row)

cursor.close()
conn.close()
