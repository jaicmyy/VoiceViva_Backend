import pymysql

def check_indices():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="voice_viva_db",
            cursorclass=pymysql.cursors.DictCursor
        )
        cursor = conn.cursor()
        cursor.execute("SHOW INDEX FROM viva_answers")
        indices = cursor.fetchall()
        for idx in indices:
            print(f"Key_name: {idx['Key_name']} | Column_name: {idx['Column_name']} | Non_unique: {idx['Non_unique']}")
            
        conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_indices()
