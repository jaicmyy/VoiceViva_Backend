from flask import Blueprint, request, jsonify, session
import pymysql

admin_auth_bp = Blueprint(
    "admin_auth",
    __name__,
    url_prefix="/api/admin"
)

def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",
        database="voice_viva_db",
        cursorclass=pymysql.cursors.DictCursor
    )

@admin_auth_bp.route("/change-password", methods=["POST"])
def change_admin_password():
    # 🔐 Auth check
    admin_id = session.get("user_id")
    role = session.get("role")

    # If session is missing (e.g. Android app restart), try Header + DB lookup
    if not admin_id:
        reg_no = request.headers.get("X-Registration-Number")
        if reg_no:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT id, role FROM users WHERE registration_number=%s", (reg_no,))
            user_auth = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_auth and user_auth["role"] == "admin":
                admin_id = user_auth["id"]
                role = "admin"

    if role != "admin" or not admin_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json() or {}
    current_pass = data.get("current")
    new_pass = data.get("new")
    confirm_pass = data.get("confirm")

    if not current_pass or not new_pass or not confirm_pass:
        return jsonify({"error": "All fields are required"}), 400

    if new_pass != confirm_pass:
        return jsonify({"error": "New passwords do not match"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password FROM users WHERE id=%s", (admin_id,))
        user = cursor.fetchone()

        if not user or user["password"] != current_pass:
            return jsonify({"error": "Current password is incorrect"}), 400

        cursor.execute("UPDATE users SET password=%s WHERE id=%s", (new_pass, admin_id))
        conn.commit()

        return jsonify({"message": "Password changed successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()
