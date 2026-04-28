import uuid
from datetime import datetime

from app.infrastructure.db import db

class AppointmentModel(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"))
    time_slot_id = db.Column(db.String, db.ForeignKey("time_slots.id"), unique=True)
    doctor_specialty_id = db.Column( db.String, db.ForeignKey("doctor_specialties.id"),nullable=False)
    status = db.Column(db.String)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    review = db.relationship("ReviewModel", backref="appointment", uselist=False)
    doctor_specialty = db.relationship("DoctorSpecialtyModel",back_populates="appointments" )