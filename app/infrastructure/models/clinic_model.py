import uuid
from datetime import datetime

from app.infrastructure.db import db

class ClinicModel(db.Model):
    __tablename__ = "clinics"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    address = db.Column(db.Text)
    phone = db.Column(db.String)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    doctors = db.relationship("DoctorModel", back_populates="clinic")