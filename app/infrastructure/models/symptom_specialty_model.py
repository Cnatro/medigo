from app.infrastructure.db import db
import uuid


class SymptomSpecialtyModel(db.Model):
    __tablename__ = "symptom_specialties"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    symptom_id = db.Column(db.String, db.ForeignKey("symptoms.id"), nullable=False,index=True)
    specialty_id = db.Column(db.String, db.ForeignKey("specialties.id"), nullable=False,index=True)
    weight = db.Column(db.Float)

    symptom = db.relationship("SymptomModel", back_populates="symptom_specialties")
    specialty = db.relationship("SpecialtyModel", back_populates="symptom_specialties")
