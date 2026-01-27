import pymysql

def update_schema():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    try:
        # Check if columns exist
        cursor.execute("DESCRIBE viva_answers")
        columns = [row['Field'] for row in cursor.fetchall()]

        if 'feedback' not in columns:
            print("Adding 'feedback' column...")
            cursor.execute("ALTER TABLE viva_answers ADD COLUMN feedback TEXT")
        else:
            print("'feedback' column already exists.")

        if 'confidence' not in columns:
            print("Adding 'confidence' column...")
            cursor.execute("ALTER TABLE viva_answers ADD COLUMN confidence FLOAT DEFAULT 0.0")
        else:
            print("'confidence' column already exists.")

        conn.commit()
        print("Schema update completed successfully.")

    except Exception as e:
        print(f"Error updating schema: {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    update_schema()
