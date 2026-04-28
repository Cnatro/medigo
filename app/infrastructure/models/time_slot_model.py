import uuid

from app.infrastructure.db import db

class TimeSlotModel(db.Model):
    __tablename__ = "time_slots"

    id = db.Column(db.String, primary_key=True,default=lambda: str(uuid.uuid4()))
    doctor_specialty_id  = db.Column(db.String, db.ForeignKey("doctor_specialties.id"), nullable=False)
    schedule_id = db.Column(db.String, db.ForeignKey("doctor_schedules.id"))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    is_available = db.Column(db.Boolean, default=True)

    appointment = db.relationship("AppointmentModel", backref="time_slot", uselist=False)
    doctor_specialty = db.relationship(
        "DoctorSpecialtyModel",
        back_populates="time_slots"
    )
    __table_args__ = (
        db.Index("idx_doctor_date_available", "doctor_specialty_id", "date", "is_available"),
    )