from app.infrastructure.db import db

class DoctorScheduleModel(db.Model):
    __tablename__ = "doctor_schedules"

    id = db.Column(db.String, primary_key=True)
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"))
    day_of_week = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    is_active = db.Column(db.Boolean, default=True)

    time_slots = db.relationship("TimeSlotModel", backref="schedule")