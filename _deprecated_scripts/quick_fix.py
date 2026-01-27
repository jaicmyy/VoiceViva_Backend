import pymysql
import sys

try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    print("✓ Database connection successful")
    
    cursor = conn.cursor()
    
    # Add generation_status
    try:
        cursor.execute("ALTER TABLE subjects ADD COLUMN generation_status ENUM('pending', 'completed', 'failed') DEFAULT 'pending'")
        conn.commit()
        print("✓ Added generation_status column")
    except pymysql.err.OperationalError as e:
        if "Duplicate column name" in str(e):
            print("✓ generation_status already exists")
        else:
            print(f"✗ Error adding generation_status: {e}")
    
    # Rename subject to subject_id
    try:
        cursor.execute("ALTER TABLE questions CHANGE COLUMN subject subject_id INT")
        conn.commit()
        print("✓ Renamed subject to subject_id")
    except pymysql.err.OperationalError as e:
        if "Unknown column" in str(e):
            print("✓ subject column doesn't exist (already renamed or never existed)")
        else:
            print(f"✗ Error renaming subject: {e}")
    
    # Rename question to question_text
    try:
        cursor.execute("ALTER TABLE questions CHANGE COLUMN question question_text TEXT")
        conn.commit()
        print("✓ Renamed question to question_text")
    except pymysql.err.OperationalError as e:
        if "Unknown column" in str(e):
            print("✓ question column doesn't exist (already renamed or never existed)")
        else:
            print(f"✗ Error renaming question: {e}")
    
    cursor.close()
    conn.close()
    print("\n✅ All done!")
    
except pymysql.err.OperationalError as e:
    print(f"❌ Database connection failed: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)
