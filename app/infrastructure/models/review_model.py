from app.infrastructure.db import db

class ReviewModel(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.String, primary_key=True)
    appointment_id = db.Column(db.String, db.ForeignKey("appointments.id"), unique=True)
    patient_id = db.Column(db.String, db.ForeignKey("patients.id"))
    doctor_id = db.Column(db.String, db.ForeignKey("doctors.id"))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime)