import uuid

from pgvector.sqlalchemy import Vector

from app.infrastructure.db import db

class SpecialtyModel(db.Model):
    __tablename__ = "specialties"

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String)
    description = db.Column(db.Text)
    embedding = db.Column(Vector(3072), nullable=True)

    doctor_specialties = db.relationship(
        "DoctorSpecialtyModel",
        back_populates="specialty"
    )

    symptom_specialties = db.relationship(
        "SymptomSpecialtyModel",
        back_populates="specialty"
    )

    # __table_args__ = (
    #     db.Index(
    #         "ix_specialties_embedding",
    #         "embedding",
    #         postgresql_using="ivfflat",
    #         postgresql_ops={"embedding": "vector_cosine_ops"},
    #         postgresql_with={"lists": 100}
    #     ),
    # )