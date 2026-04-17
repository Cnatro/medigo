import uuid
from datetime import datetime

from app.infrastructure.db import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey("patients.id"), nullable=False)
    appointment_id = db.Column(db.String, db.ForeignKey("appointments.id"), unique=True)

    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String, nullable=False, default="PENDING")

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)