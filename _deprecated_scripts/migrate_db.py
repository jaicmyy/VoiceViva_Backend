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

        # 3. Ensure 'users' table
        print("Ensuring 'users' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                registration_number VARCHAR(50) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL,
                role ENUM('admin', 'student') DEFAULT 'student',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # 4. Ensure 'student_assignments' table
        print("Ensuring 'student_assignments' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS student_assignments (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            )
        """)

        # 5. Ensure 'viva_config' table
        print("Ensuring 'viva_config' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viva_config (
                subject_id INT PRIMARY KEY,
                duration_minutes INT DEFAULT 10,
                total_marks INT DEFAULT 30,
                easy_marks INT DEFAULT 10,
                medium_marks INT DEFAULT 10,
                hard_marks INT DEFAULT 10,
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            )
        """)

        # 6. Ensure 'viva_sessions' table
        print("Ensuring 'viva_sessions' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viva_sessions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                subject_id INT NOT NULL,
                current_index INT DEFAULT 0,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (student_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (subject_id) REFERENCES subjects(id) ON DELETE CASCADE
            )
        """)

        # 7. Ensure 'viva_answers' table
        print("Ensuring 'viva_answers' table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS viva_answers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                session_id INT NOT NULL,
                question_id INT NOT NULL,
                audio_path VARCHAR(255),
                transcript TEXT,
                score INT DEFAULT 0,
                max_score INT DEFAULT 0,
                FOREIGN KEY (session_id) REFERENCES viva_sessions(id) ON DELETE CASCADE,
                FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
            )
        """)

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
