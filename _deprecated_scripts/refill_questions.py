import pymysql
from services.question_generator import generate_and_store_questions
import os

def check_and_refill():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )
    cursor = conn.cursor()

    print("Checking for subjects with missing questions...")

    try:
        # Get all viva configs
        cursor.execute("SELECT * FROM viva_config")
        configs = cursor.fetchall()
        
        for config in configs:
            subject_id = config["subject_id"]
            
            # Get subject name and syllabus
            cursor.execute("SELECT name, syllabus_pdf FROM subjects WHERE id=%s", (subject_id,))
            subject = cursor.fetchone()
            if not subject: continue
            
            name = subject["name"]
            syllabus = subject["syllabus_pdf"] # Path stored in DB
            
            if not syllabus:
                print(f"Subject {name} has no syllabus. Skipping.")
                continue
                
            # ABSOLUTE PATH FIX
            # Assuming 'uploads/syllabus' is relative to app.py, and we are in root
            # DB usually stores 'uploads/syllabus/filename.pdf' or just 'filename.pdf'
            # Let's check.
            real_path = syllabus
            if not os.path.exists(real_path):
                # Try relative
                real_path = os.path.join(os.getcwd(), syllabus)
                if not os.path.exists(real_path):
                     # Try uploads/syllabus
                     real_path = os.path.join(os.getcwd(), "uploads", "syllabus", os.path.basename(syllabus))
            
            if not os.path.exists(real_path):
                print(f"Syllabus file not found: {real_path}")
                continue

            # Check counts
            needed_total = config["easy_questions"] + config["medium_questions"] + config["hard_questions"]
            
            cursor.execute("SELECT COUNT(*) as cnt FROM questions WHERE subject_id=%s", (subject_id,))
            current_total = cursor.fetchone()["cnt"]
            
            print(f"{name}: Have {current_total} / Need {needed_total}")
            
            if current_total < needed_total:
                print(f"REFILLING {name}...")
                generate_and_store_questions(subject_id, name, real_path)
            else:
                 print(f"{name} is good.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_and_refill()
