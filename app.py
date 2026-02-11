from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

from config import Config
from extensions import db


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ===============================
    # SESSION CONFIG (CRITICAL)
    # ===============================
    app.config["SECRET_KEY"] = "super-secret-key"
    app.config["SESSION_COOKIE_SAMESITE"] = "None"
    app.config["SESSION_COOKIE_HTTPONLY"] = True
    app.config["SESSION_COOKIE_SECURE"] = False  # HTTPS only → True


    # ===============================
    # CORS CONFIG (ONLY ONCE)
    # ===============================
    CORS(app, resources={r"/*": {"origins": "*", "allow_headers": ["Content-Type", "Authorization", "X-Registration-Number"]}})


    # ===============================
    # FILE STORAGE CONFIG
    # ===============================
    BASE_DIR = os.getcwd()
    SYLLABUS_FOLDER = os.path.join(BASE_DIR, "uploads", "syllabus")
    os.makedirs(SYLLABUS_FOLDER, exist_ok=True)

    app.config["SYLLABUS_FOLDER"] = SYLLABUS_FOLDER

    # ===============================
    # INIT EXTENSIONS
    # ===============================
    db.init_app(app)

    # ===============================
    # REGISTER BLUEPRINTS
    # ===============================
    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    from routes.admin_subject_routes import admin_subject_bp
    app.register_blueprint(admin_subject_bp)

    from routes.student_assignment_routes import student_assignment_bp
    app.register_blueprint(student_assignment_bp)

    from routes.viva_config_routes import viva_config_bp
    app.register_blueprint(viva_config_bp)

    from routes.viva_session_routes import viva_session_bp
    app.register_blueprint(viva_session_bp)

    from routes.viva_report_routes import viva_report_bp
    app.register_blueprint(viva_report_bp)

    from routes.student_subject_routes import student_subject_bp
    app.register_blueprint(student_subject_bp)

    from routes.admin_auth_routes import admin_auth_bp
    app.register_blueprint(admin_auth_bp)


    # ===============================
    # PDF VIEW ROUTE
    # ===============================
    @app.route("/uploads/syllabus/<path:filename>")
    def view_syllabus_pdf(filename):
        return send_from_directory(
            app.config["SYLLABUS_FOLDER"],
            filename,
            as_attachment=False
        )

    # ===============================
    # HEALTH CHECK
    # ===============================
    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "OK",
            "message": "Voice-Based Viva Backend Running"
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
