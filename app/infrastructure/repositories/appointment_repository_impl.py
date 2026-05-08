from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from typing_extensions import override

from app.core.repositories.appointment_repository import AppointmentRepository
from app.infrastructure.db import db
from app.infrastructure.models import AppointmentModel, PatientModel, DoctorModel, DoctorSpecialtyModel
from app.infrastructure.models import PatientModel
from app.interfaces.mappers.appointment_mapper import AppointmentMapper
from app.shared.utils.appointment_enum import AppointmentStatus


class AppointmentRepositoryImpl(AppointmentRepository):
    @override
    def get_history_by_patient(self, user_id):
        patient = PatientModel.query.filter_by(user_id=user_id).first()
        models = (
            AppointmentModel.query
            .filter(
                AppointmentModel.patient_id == patient.id,
                # AppointmentModel.status.in_(["CONFIRMED", "COMPLETED"])
            )
            .order_by(AppointmentModel.created_at.desc())
            .all()
        )

        return [AppointmentMapper.model_to_entity(m) for m in models]

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

    @override
    def get_detail(self, appointment_id):
        model = (
            AppointmentModel.query
            .options(
                joinedload(AppointmentModel.doctor).joinedload(DoctorModel.user),
                joinedload(AppointmentModel.doctor).joinedload(DoctorModel.clinic),
                joinedload(AppointmentModel.doctor_specialty).joinedload(DoctorSpecialtyModel.specialty),
                joinedload(AppointmentModel.time_slot)
            )
            .filter(AppointmentModel.id == appointment_id)
            .first()
        )

        if not model:
            return None

        return AppointmentMapper.model_to_detail(model)

    @override
    def update_status(self, appointment_id, symptom: str, status):
        model = AppointmentModel.query.filter_by(id=appointment_id).first()

        if not model:
            return None

        model.status = status
        model.symptom = symptom

        db.session.commit()

        return AppointmentMapper.model_to_detail(model)