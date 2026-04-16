from typing_extensions import override

from app.core.entities.patient import Patient
from app.core.repositories.patient_repository import PatientRepository
from app.infrastructure.db import db
from app.interfaces.mappers.patient_mapper import PatientMapper


class PatientRepositoryImpl(PatientRepository):

    @override
    def save(self, patient: Patient):
        model = PatientMapper.entity_to_model(patient)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return PatientMapper.model_to_entity(model)