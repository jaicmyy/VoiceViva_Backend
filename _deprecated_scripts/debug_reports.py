import pymysql
import json
import datetime
from decimal import Decimal

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def debug_reports():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        print("Executing Query...")
        cursor.execute(
            """
            SELECT 
                vs.id,
                u.name AS student_name,
                u.registration_number,
                sub.name AS subject_name,
                (SELECT SUM(score) FROM viva_answers WHERE session_id = vs.id) AS score,
                vs.started_at AS created_at
            FROM viva_sessions vs
            JOIN users u ON vs.student_id = u.id
            JOIN subjects sub ON vs.subject_id = sub.id
            ORDER BY vs.started_at DESC
            """
        )
        reports = cursor.fetchall()
        print(f"Query returned {len(reports)} rows.")
        
        for r in reports:
            print(f"Raw Row: {r}")
            # Simulate the processing
            if r["created_at"]:
                if isinstance(r["created_at"], str):
                    print("Warning: created_at is ALREADY a string")
                else:
                    r["created_at"] = r["created_at"].strftime("%Y-%m-%d %H:%M:%S")
            else:
                r["created_at"] = "N/A"
                
            if r["score"] is None:
                r["score"] = 0
            else:
                r["score"] = int(r["score"])
                
        print("Processed Data:")
        print(json.dumps(reports, indent=2, default=str))
        
        cursor.close()
        conn.close()
        print("✅ SUCCESS: Logic seems fine.")
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    debug_reports()
