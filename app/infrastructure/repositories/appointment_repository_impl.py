from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from app.core.repositories.appointment_repository import AppointmentRepository
from app.core.repositories.doctor_repository import DoctorRepository
from app.infrastructure.db import db
from app.infrastructure.models import AppointmentModel, PatientModel, DoctorModel, DoctorSpecialtyModel
from app.interfaces.mappers.appointment_mapper import AppointmentMapper


class AppointmentRepositoryImpl(AppointmentRepository):
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

        return [AppointmentMapper.model_to_entities(m) for m in models]

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
        return AppointmentMapper.model_to_entities(model)

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