import pymysql
import sys

def check_db():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="voice_viva_db",
            cursorclass=pymysql.cursors.DictCursor
        )
        print("✅ Database connection successful")
        cursor = conn.cursor()
        
        tables = ['subjects', 'questions', 'viva_reports', 'viva_sessions', 'viva_answers', 'users']
        for table in tables:
            print(f"\n--- Columns in {table} ---")
            try:
                cursor.execute(f"SHOW COLUMNS FROM {table}")
                columns = cursor.fetchall()
                for col in columns:
                    print(f"{col['Field']}: {col['Type']} | Null: {col['Null']} | Key: {col['Key']} | Default: {col['Default']}")
            except Exception as e:
                print(f"Error checking {table}: {e}")
        
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ Connection failed: {e}")

if __name__ == "__main__":
    check_db()
