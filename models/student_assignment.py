from datetime import datetime
from app import db

class StudentAssignment(db.Model):
    __tablename__ = "student_assignments"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False
    )

    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
