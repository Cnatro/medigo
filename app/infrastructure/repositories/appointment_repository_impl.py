from sqlalchemy.exc import IntegrityError
from typing_extensions import override

from app.core.repositories.appointment_repository import AppointmentRepository
from app.infrastructure.db import db
from app.infrastructure.models import PatientModel
from app.interfaces.mappers.appointment_mapper import AppointmentMapper


class AppointmentRepositoryImpl(AppointmentRepository):
    @override
    def create(self, user_id ,appointment):
        patient = PatientModel.query.filter_by(user_id=user_id).first()
        appointment.patient_id = patient.id
        model = AppointmentMapper.entity_to_model(appointment)
        db.session.add(model)
        try:
            db.session.commit()
        except IntegrityError as e:
            db.session.rollback()
            print(f"Database Integrity Error: {e.orig}")
            return None
        return AppointmentMapper.model_to_entity(model)