from typing_extensions import override

from app.core.entities.patient import Patient
from app.core.repositories.patient_repository import PatientRepository
from app.infrastructure.db import db
from app.infrastructure.models import PatientModel
from app.interfaces.mappers.patient_mapper import PatientMapper


class PatientRepositoryImpl(PatientRepository):

    @override
    def save(self, patient: Patient):
        model = PatientMapper.entity_to_model(patient)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return PatientMapper.model_to_entity(model)

    @override
    def find_by_user_id(self, user_id):
        model = PatientModel.query.filter_by(user_id=user_id).first()

        if not model:
            return None

        return PatientMapper.model_to_entity(model)

    @override
    def update_patient_by_user_id(self, user_id, data):
        model = PatientModel.query.filter_by(user_id=user_id).first()

        if not model:
            return None

        for key, value in data.items():
            setattr(model, key, value)

        db.session.commit()
        db.session.refresh(model)

        return PatientMapper.model_to_entity(model)