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
    # def get_history_by_patient(self, user_id):
    #     patient = PatientModel.query.filter_by(user_id=user_id).first()
    #     models = (
    #         AppointmentModel.query
    #         .filter(
    #             AppointmentModel.patient_id == patient.id,
    #             # AppointmentModel.status.in_(["CONFIRMED", "COMPLETED"])
    #         )
    #         .join(DoctorModel, DoctorModel.id == AppointmentModel.doctor_id)
    #         .order_by(AppointmentModel.created_at.desc())
    #         .all()
    #     )
    #
    #     return [AppointmentMapper.model_to_entity(m) for m in models]

    def get_history_by_patient(self, user_id):

        patient = PatientModel.query.filter_by(user_id=user_id).first()

        models = (
            AppointmentModel.query
            .options(
                joinedload(AppointmentModel.review),
                joinedload(AppointmentModel.doctor)
                .joinedload(DoctorModel.user),

                joinedload(AppointmentModel.doctor)
                .joinedload(DoctorModel.clinic),

                joinedload(AppointmentModel.time_slot),

                joinedload(AppointmentModel.doctor_specialty)
                .joinedload(DoctorSpecialtyModel.specialty),

            )
            .filter(
                AppointmentModel.patient_id == patient.id
            )
            .order_by(AppointmentModel.created_at.desc())
            .all()
        )

        return [AppointmentMapper.model_to_history(m) for m in models]

    @override
    def create(self, user_id, appointment):
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

    @override
    def info_send_mail(self, appointment_id):

        model = (
            AppointmentModel.query
            .options(
                joinedload(AppointmentModel.patient)
                .joinedload(PatientModel.user),

                joinedload(AppointmentModel.doctor)
                .joinedload(DoctorModel.user),

                joinedload(AppointmentModel.time_slot),
            )
            .filter(AppointmentModel.id == appointment_id)
            .first()
        )

        if not model:
            return None

        patient_user = model.patient.user
        doctor_user = model.doctor.user
        time_slot = model.time_slot

        return {
            'patient_email': patient_user.email,

            'patient_name': patient_user.full_name,

            'doctor_name': doctor_user.full_name,

            'appointment_date': str(time_slot.date),

            'appointment_time':
                f'{time_slot.start_time} - {time_slot.end_time}',
        }
