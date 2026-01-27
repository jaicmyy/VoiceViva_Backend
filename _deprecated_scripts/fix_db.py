import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def fix_database():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Starting database fixes...")
        
        # 1. Add generation_status to subjects table
        print("\n1. Checking subjects table...")
        cursor.execute("SHOW COLUMNS FROM subjects LIKE 'generation_status'")
        if not cursor.fetchone():
            print("   Adding generation_status column...")
            cursor.execute("ALTER TABLE subjects ADD COLUMN generation_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending'")
            conn.commit()
            print("   ✓ Added generation_status")
        else:
            print("   ✓ generation_status already exists")
        
        # 2. Fix questions table - rename subject to subject_id
        print("\n2. Checking questions table...")
        cursor.execute("SHOW COLUMNS FROM questions LIKE 'subject_id'")
        if not cursor.fetchone():
            cursor.execute("SHOW COLUMNS FROM questions LIKE 'subject'")
            if cursor.fetchone():
                print("   Renaming 'subject' to 'subject_id'...")
                cursor.execute("ALTER TABLE questions CHANGE COLUMN subject subject_id INT")
                conn.commit()
                print("   ✓ Renamed subject to subject_id")
            else:
                print("   Adding subject_id column...")
                cursor.execute("ALTER TABLE questions ADD COLUMN subject_id INT")
                conn.commit()
                print("   ✓ Added subject_id")
        else:
            print("   ✓ subject_id already exists")
        
        # 3. Fix questions table - rename question to question_text
        cursor.execute("SHOW COLUMNS FROM questions LIKE 'question_text'")
        if not cursor.fetchone():
            cursor.execute("SHOW COLUMNS FROM questions LIKE 'question'")
            if cursor.fetchone():
                print("   Renaming 'question' to 'question_text'...")
                cursor.execute("ALTER TABLE questions CHANGE COLUMN question question_text TEXT")
                conn.commit()
                print("   ✓ Renamed question to question_text")
            else:
                print("   Adding question_text column...")
                cursor.execute("ALTER TABLE questions ADD COLUMN question_text TEXT")
                conn.commit()
                print("   ✓ Added question_text")
        else:
            print("   ✓ question_text already exists")
        
        print("\n✅ Database fixes completed successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"\n❌ Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    fix_database()
