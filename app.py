from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    from routes.admin_subject_routes import admin_subject_bp
    app.register_blueprint(admin_subject_bp)
    from routes.student_assignment_routes import student_assign_bp
    app.register_blueprint(student_assign_bp)
    from routes.viva_config_routes import viva_config_bp
    app.register_blueprint(viva_config_bp)
    from routes.viva_session_routes import viva_session_bp
    app.register_blueprint(viva_session_bp)
    from routes.viva_report_routes import viva_report_bp
    app.register_blueprint(viva_report_bp)





    CORS(app)
    db.init_app(app)

    from routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp)

    @app.route("/", methods=["GET"])
    def health_check():
        return jsonify({
            "status": "OK",
            "message": "Voice-Based Viva Backend Running"
        })

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
