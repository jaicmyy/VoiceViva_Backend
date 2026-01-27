import pymysql

def check_schema():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="voice_viva_db",
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("DESCRIBE viva_answers")
        columns = cursor.fetchall()
        for col in columns:
            print(f"{col['Field']} | Type: {col['Type']} | Null: {col['Null']} | Default: {col['Default']}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_schema()
