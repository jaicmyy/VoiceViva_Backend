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
        cursor.execute("DESCRIBE questions")
        columns = cursor.fetchall()
        for col in columns:
            print(f"Field: {col['Field']}, Type: {col['Type']}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_schema()
