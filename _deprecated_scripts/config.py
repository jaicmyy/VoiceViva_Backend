import os

class Config:
    SECRET_KEY = "dev-secret-key"

    # MySQL Configuration (XAMPP)
    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = ""     # default XAMPP password
    MYSQL_DB = "voice_viva_db"

    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://root:@localhost/voice_viva_db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    SYLLABUS_FOLDER = os.path.join(UPLOAD_FOLDER, "syllabus_pdfs")
    AUDIO_FOLDER = os.path.join(UPLOAD_FOLDER, "audio_answers")
    REPORT_FOLDER = os.path.join(os.getcwd(), "reports", "generated_reports")
