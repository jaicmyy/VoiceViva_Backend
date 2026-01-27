from flask import Blueprint, request, jsonify, session
import pymysql

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )


from flask import Blueprint, request, jsonify, session

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    registration_number = data.get("registration_number")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, role, registration_number, name
        FROM users
        WHERE registration_number=%s AND password=%s
    """, (registration_number, password))

    user = cursor.fetchone()
    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    # ✅ THIS IS CRITICAL
    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]
    session["registration_number"] = user["registration_number"]

    print("SESSION CREATED:", dict(session))  # DEBUG

    return jsonify({
        "message": "Login successful",
        "role": user["role"],
        "name": user["name"],
        "registration_number": user["registration_number"]
    })
