import pymysql

def read_db():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()
    
    try:
        print("--- Tables in voice_viva_db ---")
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
            table_name = list(table.values())[0]
            cursor.execute(f"SELECT COUNT(*) as count FROM `{table_name}`")
            count = cursor.fetchone()['count']
            print(f"Table: {table_name}, Rows: {count}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    read_db()
