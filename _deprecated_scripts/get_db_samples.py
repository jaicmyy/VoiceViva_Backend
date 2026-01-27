import pymysql

def get_samples():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    
    try:
        print("\n--- Recent Subjects ---")
        cursor.execute("SELECT id, name, code FROM subjects ORDER BY id DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"[{row['id']}] {row['name']} ({row['code']})")

        print("\n--- Sample Questions ---")
        cursor.execute("SELECT q.id, s.name as subject, q.difficulty, q.question_text FROM questions q JOIN subjects s ON q.subject_id = s.id ORDER BY q.id DESC LIMIT 5")
        for row in cursor.fetchall():
            print(f"[{row['id']}] {row['subject']} | {row['difficulty']} | {row['question_text'][:80]}...")

        print("\n--- User Roles ---")
        cursor.execute("SELECT role, COUNT(*) as count FROM users GROUP BY role")
        for row in cursor.fetchall():
            print(f"Role: {row['role']}, Count: {row['count']}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    get_samples()
