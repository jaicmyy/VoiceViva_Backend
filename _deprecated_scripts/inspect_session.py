import pymysql

def inspect_session():
    conn = pymysql.connect(host="localhost", user="root", password="", database="voice_viva_db", cursorclass=pymysql.cursors.DictCursor)
    cursor = conn.cursor()

    # Get one session with a report
    cursor.execute("""
        SELECT vs.id, vs.easy_q_ids, vs.medium_q_ids, vs.hard_q_ids, vr.total_questions, vr.max_total_score
        FROM viva_sessions vs
        LEFT JOIN viva_reports vr ON vs.id = vr.session_id
    """)
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} sessions.")
    for row in rows:
        print(f"Session {row['id']}: Easy='{row['easy_q_ids']}', Med='{row['medium_q_ids']}', Hard='{row['hard_q_ids']}'")

    
    if row:
        print(f"Session ID: {row['id']}")
        e = str(row['easy_q_ids']).split(',') if row['easy_q_ids'] else []
        m = str(row['medium_q_ids']).split(',') if row['medium_q_ids'] else []
        h = str(row['hard_q_ids']).split(',') if row['hard_q_ids'] else []
        
        # Filter empty strings
        e = [x for x in e if x]
        m = [x for x in m if x]
        h = [x for x in h if x]

        count = len(e) + len(m) + len(h)
        print(f"Assigned Questions (Easy+Med+Hard): {count}")
        print(f"Stored in Report (total_questions): {row['total_questions']}")
        print(f"Stored Max Score: {row['max_total_score']}")
    else:
        print("No reports found.")

    conn.close()

if __name__ == "__main__":
    inspect_session()
