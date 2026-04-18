from app.infrastructure.db import db

class SymptomSpecialtyModel(db.Model):
    __tablename__ = "symptom_specialties"

    symptom_id = db.Column(db.String, db.ForeignKey("symptoms.id"), primary_key=True)
    specialty_id = db.Column(db.String, db.ForeignKey("specialties.id"), primary_key=True)
    weight = db.Column(db.Float)