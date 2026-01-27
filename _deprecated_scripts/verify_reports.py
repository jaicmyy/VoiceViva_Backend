import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

def verify_reports():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. Get all submitted sessions
    cursor.execute("""
        SELECT vs.id, vs.subject_id, vs.student_id, u.registration_number
        FROM viva_sessions vs
        JOIN users u ON vs.student_id = u.id
        WHERE vs.is_submitted = 1
    """)
    sessions = cursor.fetchall()
    
    print(f"Found {len(sessions)} submitted sessions.")
    print("-" * 60)
    print(f"{'Student':<15} | {'Answers':<8} | {'Score (DB)':<10} | {'Max (DB)':<10} | {'Status'}")
    print("-" * 60)

    for s in sessions:
        session_id = s['id']
        reg_no = s['registration_number']
        
        # 2. Count actual answers in viva_answers
        cursor.execute("SELECT COUNT(*) as cnt, SUM(score) as total_score, SUM(max_score) as total_max FROM viva_answers WHERE session_id=%s", (session_id,))
        ans_data = cursor.fetchone()
        
        actual_count = ans_data['cnt']
        actual_score = ans_data['total_score'] or 0.0
        actual_max = ans_data['total_max'] or 0.0
        
        # 3. Get stored report data (if available)
        cursor.execute("SELECT total_questions, total_score, max_total_score FROM viva_reports WHERE session_id=%s", (session_id,))
        rep_data = cursor.fetchone()
        
        report_count = rep_data['total_questions'] if rep_data else "N/A"
        report_score = rep_data['total_score'] if rep_data else "N/A"
        report_max = rep_data['max_total_score'] if rep_data else "N/A"

        # 4. Compare
        status = "OK"
        if report_count != "N/A":
             # We want strict equality on counts
             if actual_count != report_count:
                 status = f"MISMATCH: Answers={actual_count}, Report={report_count}"
             # Float comparison with small tolerance
             elif abs(float(actual_score) - float(report_score)) > 0.1:
                 status = f"MISMATCH: Score={actual_score}, Report={report_score}"
        else:
             status = "NO REPORT ENTRY"

        print(f"{reg_no:<15} | {actual_count:<8} | {actual_score:<10} | {actual_max:<10} | {status}")

    conn.close()

if __name__ == "__main__":
    verify_reports()
