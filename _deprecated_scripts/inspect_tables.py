import pymysql

def check_schema():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    
    try:
        print("--- viva_sessions ---")
        cursor.execute("DESCRIBE viva_sessions")
        for col in cursor.fetchall():
            print(f"Field: {col['Field']}, Type: {col['Type']}")
            
        print("\n--- viva_reports ---")
        cursor.execute("DESCRIBE viva_reports")
        for col in cursor.fetchall():
            print(f"Field: {col['Field']}, Type: {col['Type']}")
            
        print("\n--- viva_answers ---")
        cursor.execute("DESCRIBE viva_answers")
        for col in cursor.fetchall():
            print(f"Field: {col['Field']}, Type: {col['Type']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_schema()
