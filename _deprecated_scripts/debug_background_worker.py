
# ----------------------------------------------------
# DEBUGGER SCRIPT TO RUN BACKGROUND LOGIC MANUALLY
# ----------------------------------------------------
import os
import sys

# Add current directory to path so we can import modules
sys.path.append(os.getcwd())

from routes.viva_session_routes import process_answer_background
import pymysql

# CONFIG
SESSION_ID = 10001
QUESTION_ID = 348
AUDIO_PATH = "uploads/audio_answers/dummy_debug.3gp" # We will create a dummy file
MAX_MARKS = 2
QUESTION_TEXT = "What is debugging?"
CONCEPTS = "Finding and fixing errors"

# Create dummy audio file if not exists
if not os.path.exists("uploads/audio_answers"):
    os.makedirs("uploads/audio_answers")

with open(AUDIO_PATH, "wb") as f:
    f.write(b"dummy audio content")

print("Starting Manual Background Process...")
try:
    process_answer_background(SESSION_ID, QUESTION_ID, AUDIO_PATH, MAX_MARKS, QUESTION_TEXT, CONCEPTS)
    print("Finished without exception.")
except Exception as e:
    print(f"CRITICAL ERROR CAUGHT: {e}")
    import traceback
    traceback.print_exc()

# Check DB result
conn = pymysql.connect(host="localhost", user="root", password="", database="voice_viva_db", cursorclass=pymysql.cursors.DictCursor)
cur = conn.cursor()
cur.execute("SELECT status, score, transcript FROM viva_answers WHERE session_id=%s AND question_id=%s", (SESSION_ID, QUESTION_ID))
print("DB STATE:", cur.fetchone())
conn.close()
