import pymysql

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

conn = get_db_connection()
cursor = conn.cursor()

print("Columns in subjects:")
cursor.execute("DESCRIBE subjects")
for col in cursor.fetchall():
    print(f"- {col['Field']} ({col['Type']})")

cursor.close()
conn.close()
