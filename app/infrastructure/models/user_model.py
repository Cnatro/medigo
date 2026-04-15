import uuid
from app.infrastructure.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    phone = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    doctor = db.relationship("DoctorModel", back_populates="user", uselist=False)
    patient = db.relationship("PatientModel", back_populates="user", uselist=False)