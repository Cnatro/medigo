import uuid

from pygments.lexer import default

from app.infrastructure.db import db

class DoctorScheduleModel(db.Model):
    __tablename__ = "doctor_schedules"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    doctor_specialty_id = db.Column(db.String, db.ForeignKey("doctor_specialties.id"), nullable=False)
    day_of_week = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)
    type = db.Column(db.String,default="REGULAR") # REGULAR EXTRA_SHIFT WEEKEND_SHIFT
    status = db.Column(db.String, default= "ACTIVE") # ACTIVE LEAVE_PENDING LEAVE_APPROVED CANCELLED
    reason = db.Column(db.Text, default=None)

    time_slots = db.relationship("TimeSlotModel", backref="schedule")
    doctor_specialty = db.relationship(
        "DoctorSpecialtyModel",
        back_populates="schedules"
    )