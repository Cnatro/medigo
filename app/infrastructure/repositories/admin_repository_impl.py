from datetime import datetime, timedelta

from sqlalchemy import func, extract, desc
from sqlalchemy.orm import aliased
from typing_extensions import override

from app.core.repositories.admin_repository import AdminRepository
from app.infrastructure.db import db
from app.infrastructure.models import (
    PatientModel,
    AppointmentModel,
    ReviewModel,
    DoctorModel,
    UserModel,
    DoctorSpecialtyModel,
    SpecialtyModel,
    TimeSlotModel, ClinicModel, DoctorScheduleModel, OrderModel, PaymentTransactionModel
)
from app.shared.utils.schedule_enum import ScheduleStatus


class AdminRepositoryImpl(AdminRepository):

    @override
    def get_dashboard_stats(self):
        current_month = datetime.now().month
        current_year = datetime.now().year

        total_patients = db.session.query(
            func.count(PatientModel.id)
        ).scalar()

        monthly_appointments = db.session.query(
            func.count(AppointmentModel.id)
        ).filter(
            extract("month", AppointmentModel.created_at) == current_month,
            extract("year", AppointmentModel.created_at) == current_year
        ).scalar()

        avg_rating = db.session.query(
            func.avg(ReviewModel.rating)
        ).scalar()

        satisfaction_rate = round((avg_rating / 5) * 100, 2) if avg_rating else 0

        return {
            "total_patients": total_patients,
            "monthly_appointments": monthly_appointments,
            "average_wait_time": None,
            "satisfaction_rate": satisfaction_rate
        }

    @override
    def get_weekly_appointments(self):
        today = datetime.today()
        start_week = today - timedelta(days=today.weekday())
        end_week = start_week + timedelta(days=6)

        results = (
            db.session.query(
                func.date(AppointmentModel.created_at).label("date"),
                func.count(AppointmentModel.id).label("appointments")
            )
            .filter(
                AppointmentModel.created_at >= start_week,
                AppointmentModel.created_at <= end_week
            )
            .group_by(func.date(AppointmentModel.created_at))
            .all()
        )

        return [
            {
                "day": str(item.date),
                "appointments": item.appointments
            }
            for item in results
        ]

    @override
    def get_top_doctors(self):
        results = (
            db.session.query(
                DoctorModel.id,
                UserModel.full_name,
                SpecialtyModel.name.label("specialty"),
                DoctorModel.rating_avg,
                func.count(AppointmentModel.id).label("patients")
            )
            .join(UserModel, UserModel.id == DoctorModel.user_id)
            .join(
                DoctorSpecialtyModel,
                DoctorSpecialtyModel.doctor_id == DoctorModel.id
            )
            .join(
                SpecialtyModel,
                SpecialtyModel.id == DoctorSpecialtyModel.specialty_id
            )
            .outerjoin(
                AppointmentModel,
                AppointmentModel.doctor_id == DoctorModel.id
            )
            .group_by(
                DoctorModel.id,
                UserModel.full_name,
                SpecialtyModel.name
            )
            .order_by(
                desc(DoctorModel.rating_avg),
                desc(func.count(AppointmentModel.id))
            )
            .limit(5)
            .all()
        )

        return [
            {
                "doctor_id": item.id,
                "doctor_name": item.full_name,
                "specialty": item.specialty,
                "rating": item.rating_avg,
                "patients": item.patients
            }
            for item in results
        ]

    @override
    def get_recent_appointments(self):
        patient_user = aliased(UserModel)
        doctor_user = aliased(UserModel)

        results = (
            db.session.query(
                AppointmentModel.id,
                AppointmentModel.status,
                AppointmentModel.created_at,

                patient_user.full_name.label("patient_name"),
                doctor_user.full_name.label("doctor_name"),

                DoctorModel.id.label("doctor_id"),
                SpecialtyModel.name.label("specialty")
            )
            # patient
            .join(
                PatientModel,
                PatientModel.id == AppointmentModel.patient_id
            )
            .join(
                patient_user,
                patient_user.id == PatientModel.user_id
            )

            # doctor
            .join(
                DoctorModel,
                DoctorModel.id == AppointmentModel.doctor_id
            )
            .join(
                doctor_user,
                doctor_user.id == DoctorModel.user_id
            )

            # specialty
            .join(
                DoctorSpecialtyModel,
                DoctorSpecialtyModel.id == AppointmentModel.doctor_specialty_id
            )
            .join(
                SpecialtyModel,
                SpecialtyModel.id == DoctorSpecialtyModel.specialty_id
            )

            .order_by(desc(AppointmentModel.created_at))
            .limit(10)
            .all()
        )

        return [
            {
                "appointment_id": item.id,
                "patient_name": item.patient_name,
                "doctor_name": item.doctor_name,
                "doctor_id": item.doctor_id,
                "specialty": item.specialty,
                "date_time": item.created_at,
                "status": item.status
            }
            for item in results
        ]

    @override
    def get_all_users(self):
        return UserModel.query.all()

    @override
    def get_all_clinics(self):
        return ClinicModel.query.all()

    @override
    def get_all_schedules(self):
        return DoctorScheduleModel.query.all()

    @override
    def get_all_orders(self):
        return OrderModel.query.all()

    @override
    def get_all_payment_transactions(self):
        return (
            db.session.query(
                PaymentTransactionModel.id,
                PaymentTransactionModel.order_id,
                PaymentTransactionModel.provider,
                PaymentTransactionModel.transaction_code,
                PaymentTransactionModel.amount,
                PaymentTransactionModel.status,
                PaymentTransactionModel.type,
                PaymentTransactionModel.created_at,

                UserModel.full_name.label("patient_name")
            )
            .join(
                OrderModel,
                OrderModel.id == PaymentTransactionModel.order_id
            )
            .join(
                PatientModel,
                PatientModel.id == OrderModel.patient_id
            )
            .join(
                UserModel,
                UserModel.id == PatientModel.user_id
            )
            .order_by(desc(PaymentTransactionModel.created_at))
            .all()
        )

    @override
    def get_schedule_pending_requests(self):
        return (
            DoctorScheduleModel.query
            .filter(
                DoctorScheduleModel.status.in_([ScheduleStatus.LEAVE_PENDING.name,ScheduleStatus.EXTRA_PENDING.name,ScheduleStatus.WEEKEND_PENDING.name])
            )
            .order_by(desc(DoctorScheduleModel.id))
            .all()
        )
