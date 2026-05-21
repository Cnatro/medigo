import uuid
from datetime import datetime

from app.infrastructure.db import db
from sqlalchemy.dialects.postgresql import JSONB

class ChatSessionModel(db.Model):
    __tablename__ = "chat_sessions"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    patient_id = db.Column(db.String, db.ForeignKey("patients.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    messages = db.relationship("ChatMessageModel", backref="session")


class ChatMessageModel(db.Model):
    __tablename__ = "chat_messages"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = db.Column(db.String, db.ForeignKey("chat_sessions.id"))
    sender = db.Column(db.String)
    message = db.Column(JSONB)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)