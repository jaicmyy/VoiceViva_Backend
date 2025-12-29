from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
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


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    registration_number = data.get("registration_number")
    password = data.get("password")

    if not registration_number or not password:
        return jsonify({"error": "All fields are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE registration_number = %s",
        (registration_number,)
    )
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    if not check_password_hash(user["password_hash"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "registration_number": user["registration_number"],
            "role": user["role"],
            "name": user["name"]
        }
    }), 200
