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
from app.interfaces.mappers.doctor_mapper import DoctorMapper
from app.shared.utils.role import Role
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
        today = datetime.today().date()

        last_7_days = [
            today - timedelta(days=i)
            for i in range(6, -1, -1)
        ]

        db_result = (
            db.session.query(
                func.date(AppointmentModel.created_at).label("date"),
                func.count(AppointmentModel.id).label("appointments")
            )
            .filter(
                AppointmentModel.created_at >= last_7_days[0]
            )
            .group_by(func.date(AppointmentModel.created_at))
            .all()
        )

        appointment_map = {
            item.date: item.appointments
            for item in db_result
        }

        return [
            {
                "day": day.strftime("%d/%m"),
                "appointments": appointment_map.get(day, 0)
            }
            for day in last_7_days
        ]

    @override
    def get_top_doctors(self):
        results = (
            db.session.query(
                DoctorModel.id,
                UserModel.full_name,
                DoctorModel.rating_avg,
                func.count(AppointmentModel.id).label("patients")
            )
            .join(UserModel, UserModel.id == DoctorModel.user_id)
            .outerjoin(
                AppointmentModel,
                AppointmentModel.doctor_id == DoctorModel.id
            )
            .group_by(
                DoctorModel.id,
                UserModel.full_name,
                DoctorModel.rating_avg
            )
            .order_by(
                desc(func.count(AppointmentModel.id)),
                desc(DoctorModel.rating_avg)
            )
            .limit(5)
            .all()
        )

        return [
            {
                "doctor_id": item.id,
                "doctor_name": item.full_name,
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
    def get_all_users(self, page, limit, filters):
        query = UserModel.query.filter(
            UserModel.role != Role.ADMIN.name
        )

        if filters.get("search"):
            search = filters["search"]

            query = query.filter(
                db.or_(
                    UserModel.full_name.ilike(f"%{search}%"),
                    UserModel.email.ilike(f"%{search}%")
                )
            )

        if filters.get("role"):
            query = query.filter(
                UserModel.role == filters["role"]
            )

        return query.order_by(
            UserModel.created_at.desc()
        ).paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

    @override
    def get_all_clinics(self):
        return ClinicModel.query.all()

    @override
    def get_all_schedules(self, page, limit, filters):
        query = DoctorModel.query \
            .join(
            UserModel,
            DoctorModel.user_id == UserModel.id
        )

        if filters.get("doctor_name"):
            query = query.filter(
                UserModel.full_name.ilike(
                    f"%{filters['doctor_name']}%"
                )
            )

        if filters.get("clinic_id"):
            query = query.filter(
                DoctorModel.clinic_id == filters["clinic_id"]
            )

        if filters.get("specialty_id"):
            query = query.join(
                DoctorSpecialtyModel,
                DoctorSpecialtyModel.doctor_id == DoctorModel.id
            ).filter(
                DoctorSpecialtyModel.specialty_id == filters["specialty_id"]
            )

        return query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )

    @override
    def get_all_orders(self):
        return OrderModel.query.all()

    @override
    def get_all_payment_transactions(self, page=None, limit=None):
        query = (
            db.session.query(
                PaymentTransactionModel.id,
                PaymentTransactionModel.order_id,
                PaymentTransactionModel.provider,
                PaymentTransactionModel.transaction_code,
                PaymentTransactionModel.amount,
                PaymentTransactionModel.status,
                PaymentTransactionModel.type,
                PaymentTransactionModel.created_at,
                PaymentTransactionModel.logs,

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
        )

        if page is not None and limit is not None:
            query = query.limit(limit).offset((page - 1) * limit)

        return query.all()

    @override
    def get_schedule_pending_requests(self):
        return (
            DoctorScheduleModel.query
            .filter(
                DoctorScheduleModel.status.in_([ScheduleStatus.LEAVE_PENDING.name, ScheduleStatus.EXTRA_PENDING.name,
                                                ScheduleStatus.WEEKEND_PENDING.name])
            )
            .order_by(desc(DoctorScheduleModel.id))
            .all()
        )

    @override
    def get_doctor_detail_to_gen_calender(self, doctor_id):
        result = db.session.query(
            DoctorModel, UserModel, ClinicModel, SpecialtyModel, DoctorSpecialtyModel
        ).join(UserModel, UserModel.id == DoctorModel.user_id) \
            .join(ClinicModel, ClinicModel.id == DoctorModel.clinic_id) \
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.doctor_id == DoctorModel.id) \
            .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id) \
            .filter(DoctorModel.id == doctor_id) \
            .all()

        if not result:
            return None

        return DoctorMapper.map_doctors(result)

    @override
    def get_revenue_chart(self):
        today = datetime.today().date()

        last_7_days = [
            today - timedelta(days=i)
            for i in range(6, -1, -1)
        ]

        results = (
            db.session.query(
                func.date(PaymentTransactionModel.created_at).label("date"),
                func.sum(PaymentTransactionModel.amount).label("revenue")
            )
            .filter(
                PaymentTransactionModel.status == "SUCCESS",
                PaymentTransactionModel.type == "PAYMENT",
                PaymentTransactionModel.created_at >= last_7_days[0]
            )
            .group_by(
                func.date(PaymentTransactionModel.created_at)
            )
            .all()
        )

        revenue_map = {
            item.date: float(item.revenue or 0)
            for item in results
        }

        return [
            {
                "day": day.strftime("%d/%m"),
                "revenue": revenue_map.get(day, 0)
            }
            for day in last_7_days
        ]

    @override
    def get_appointment_status_summary(self):
        results = (
            db.session.query(
                AppointmentModel.status,
                func.count(AppointmentModel.id)
            )
            .group_by(AppointmentModel.status)
            .all()
        )

        return {
            item[0]: item[1]
            for item in results
        }
