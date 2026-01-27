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

cursor.execute("DESCRIBE viva_answers")
columns = cursor.fetchall()

print("Columns in viva_answers:")
for col in columns:
    print(f"- {col['Field']} ({col['Type']})")

cursor.close()
conn.close()
