import uuid
from datetime import datetime

from app.infrastructure.db import db

class PatientModel(db.Model):
    __tablename__ = "patients"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("users.id"), unique=True)
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("UserModel", back_populates="patient")
    appointments = db.relationship("AppointmentModel", backref="patient")