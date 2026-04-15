from app.infrastructure.db import db

class SymptomModel(db.Model):
    __tablename__ = "symptoms"

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.Text)
    embedding = db.Column(db.Text)