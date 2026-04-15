from app.infrastructure.db import db

class AppointmentModel(db.Model):
    __tablename__ = "appointments"

    id = db.Column(db.String, primary_key=True)
    patient_id = db.Column(db.String, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"))
    time_slot_id = db.Column(db.String, db.ForeignKey("time_slots.id"), unique=True)
    status = db.Column(db.String)
    reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    review = db.relationship("ReviewModel", backref="appointment", uselist=False)