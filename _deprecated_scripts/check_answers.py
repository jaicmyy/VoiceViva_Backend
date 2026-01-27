import pymysql

def check_answers():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="voice_viva_db",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("[OK] Database connected.")
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM viva_answers ORDER BY answered_at DESC LIMIT 5")
        rows = cursor.fetchall()
        
        if not rows:
            print("[INFO] No answers found in 'viva_answers' table.")
        else:
            print(f"[OK] Found {len(rows)} recent answers:")
            for row in rows:
                print("-" * 40)
                print(f"Session: {row.get('session_id')} | Q: {row.get('question_id')}")
                print(f"Time: {row.get('answered_at')}")
                print(f"Score: {row.get('score')} / {row.get('max_score')}")
                print(f"Path: {row.get('audio_path')}")
                # Print first 50 chars of transcript to keep it clean
                trans = row.get('transcript') or ""
                print(f"Transcript: {trans[:50]}...") 
                print(f"Confidence: {row.get('confidence')}")
                
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    check_answers()
