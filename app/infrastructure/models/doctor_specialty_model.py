import uuid

from app.infrastructure.db import db

class DoctorSpecialtyModel(db.Model):
    __tablename__ = "doctor_specialties"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"), nullable=False)
    specialty_id = db.Column(db.String, db.ForeignKey("specialties.id"), nullable=False)
    consultation_fee = db.Column(db.Numeric(precision=12, scale=2), default=0)

    appointments = db.relationship("AppointmentModel", back_populates="doctor_specialty")
    doctor = db.relationship("DoctorModel", back_populates="doctor_specialties")
    specialty = db.relationship("SpecialtyModel", back_populates="doctor_specialties")

    schedules = db.relationship(
        "DoctorScheduleModel",
        back_populates="doctor_specialty"
    )

    time_slots = db.relationship(
        "TimeSlotModel",
        back_populates="doctor_specialty"
    )