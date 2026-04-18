import uuid

from app.infrastructure.db import db

class SpecialtyModel(db.Model):
    __tablename__ = "specialties"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    description = db.Column(db.Text)
    embedding = db.Column(db.Text)

    doctors = db.relationship(
        "DoctorModel",
        secondary="doctor_specialties",
        backref="specialties"
    )