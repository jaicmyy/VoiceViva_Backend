import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def migrate():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        print("Starting migration...")

        # 1. Update 'subjects' table
        print("Updating 'subjects' table...")
        cursor.execute("SHOW COLUMNS FROM subjects LIKE 'generation_status'")
        if not cursor.fetchone():
            cursor.execute("ALTER TABLE subjects ADD COLUMN generation_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending'")
            print("Added 'generation_status' to 'subjects'")
        else:
            print("'generation_status' already exists in 'subjects'")

        # 2. Update 'questions' table
        print("Updating 'questions' table...")
        # Check if 'subject_id' exists
        cursor.execute("SHOW COLUMNS FROM questions LIKE 'subject_id'")
        if not cursor.fetchone():
            # If 'subject' exists, rename or just add subject_id
            cursor.execute("SHOW COLUMNS FROM questions LIKE 'subject'")
            if cursor.fetchone():
                cursor.execute("ALTER TABLE questions CHANGE COLUMN subject subject_id INT")
                print("Renamed 'subject' to 'subject_id' in 'questions'")
            else:
                cursor.execute("ALTER TABLE questions ADD COLUMN subject_id INT")
                print("Added 'subject_id' to 'questions'")
        
        # Check if 'question_text' exists
        cursor.execute("SHOW COLUMNS FROM questions LIKE 'question_text'")
        if not cursor.fetchone():
            cursor.execute("SHOW COLUMNS FROM questions LIKE 'question'")
            if cursor.fetchone():
                cursor.execute("ALTER TABLE questions CHANGE COLUMN question question_text TEXT")
                print("Renamed 'question' to 'question_text' in 'questions'")
            else:
                cursor.execute("ALTER TABLE questions ADD COLUMN question_text TEXT")
                print("Added 'question_text' to 'questions'")

        # 3. Rename 'answers' to 'viva_answers' if it exists and is needed
        # Actually, the code uses "INSERT INTO answers" in viva_session_routes.py (Line 204)
        # But the database has 'viva_answers'. 
        # I should probably just make sure the table exists as 'answers' or 'viva_answers'
        # and update the code to match what we want.
        # Let's keep 'viva_answers' and update the code.
        
        # 4. Ensure foreign keys for subjects -> questions
        try:
            cursor.execute("ALTER TABLE questions ADD CONSTRAINT fk_subject FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE")
            print("Added foreign key constraint to 'questions'")
        except Exception as e:
            print(f"Note: Could not add foreign key (maybe already exists or data mismatch): {e}")

        conn.commit()
        print("Migration completed successfully!")

    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    migrate()
