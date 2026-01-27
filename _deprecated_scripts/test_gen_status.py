import pymysql
import sys

# Change default encoding to utf-8 for stdout
sys.stdout.reconfigure(encoding='utf-8')

def test_generation():
    print("Testing Generation Logic...")
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    
    # Check counts
    cursor.execute("""
        SELECT s.name, 
               (SELECT COUNT(*) FROM questions WHERE subject_id=s.id) as q_count 
        FROM subjects s
    """)
    rows = cursor.fetchall()
    
    print("\nCurrent Question Counts:")
    for row in rows:
        print(f"Subject: {row['name']} | Questions: {row['q_count']}")
        
    print("\nIf counts match your config (e.g. 19), generation is working.")
    
    conn.close()

if __name__ == "__main__":
    test_generation()
