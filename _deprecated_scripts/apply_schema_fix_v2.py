import pymysql

def apply_fix():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db"
    )
    cursor = conn.cursor()
    
    try:
        with open("schema_fix_v2.sql", "r") as f:
            sql = f.read()
            for statement in sql.split(";"):
                if statement.strip():
                    cursor.execute(statement)
        conn.commit()
        print("Schema fix applied successfully!")
    except Exception as e:
        print(f"Error applying schema fix: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    apply_fix()
