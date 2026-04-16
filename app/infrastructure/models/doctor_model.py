import uuid
from datetime import datetime

from app.infrastructure.db import db

class DoctorModel(db.Model):
    __tablename__ = "doctors"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String, db.ForeignKey("users.id"), unique=True)
    bio = db.Column(db.Text)
    experience_years = db.Column(db.Integer)
    clinic_id = db.Column(db.String, db.ForeignKey("clinics.id"))
    rating_avg = db.Column(db.Float, default=0)
    total_reviews = db.Column(db.Integer, default=0)
    embedding = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("UserModel", back_populates="doctor")
    clinic = db.relationship("ClinicModel", back_populates="doctors")

    schedules = db.relationship("DoctorScheduleModel", backref="doctor")
    time_slots = db.relationship("TimeSlotModel", backref="doctor")
    appointments = db.relationship("AppointmentModel", backref="doctor")