from app.infrastructure.db import db

class DoctorSpecialtyModel(db.Model):
    __tablename__ = "doctor_specialties"

    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"), primary_key=True)
    specialty_id = db.Column(db.String, db.ForeignKey("specialties.id"), primary_key=True)
    consultation_fee = db.Column(db.Numeric(precision=12, scale=2), default=0)