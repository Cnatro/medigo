from app.infrastructure.db import db

class TimeSlotModel(db.Model):
    __tablename__ = "time_slots"

    id = db.Column(db.String, primary_key=True)
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"))
    schedule_id = db.Column(db.String, db.ForeignKey("doctor_schedules.id"))
    date = db.Column(db.Date)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    is_available = db.Column(db.Boolean, default=True)

    appointment = db.relationship("AppointmentModel", backref="time_slot", uselist=False)

    __table_args__ = (
        db.Index("idx_doctor_date_available", "doctor_id", "date", "is_available"),
    )