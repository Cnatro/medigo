from app.infrastructure.repositories.admin_repository_impl import AdminRepositoryImpl
from app.shared.utils.message_code import MessageCode
from app.shared.utils.role import Role
from app.shared.utils.schedule_enum import ScheduleType, ScheduleStatus


class AdminQueryService:

    def __init__(self, admin_repo: AdminRepositoryImpl):
        self.admin_repo = admin_repo

    def get_dashboard_stats(self):
        result = self.admin_repo.get_dashboard_stats()
        return result, MessageCode.SUCCESS

    def get_weekly_appointments(self):
        result = self.admin_repo.get_weekly_appointments()
        return result, MessageCode.SUCCESS

    def get_top_doctors(self):
        result = self.admin_repo.get_top_doctors()
        return result, MessageCode.SUCCESS

    def get_recent_appointments(self):
        result = self.admin_repo.get_recent_appointments()
        return result, MessageCode.SUCCESS

    def get_dashboard_overview(self):
        return {
            "stats": self.admin_repo.get_dashboard_stats(),
            "weekly_appointments": self.admin_repo.get_weekly_appointments(),
            "revenue_chart": self.admin_repo.get_revenue_chart(),
            "appointment_status_summary": self.admin_repo.get_appointment_status_summary(),
            "top_doctors": self.admin_repo.get_top_doctors(),
            "recent_appointments": self.admin_repo.get_recent_appointments()
        }, MessageCode.SUCCESS

    def get_users(self, page, limit, filters):
        users_page = self.admin_repo.get_all_users(
            page=page,
            limit=limit,
            filters=filters
        )

        users = users_page.items

        result = [
            {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "status": "active" if user.created_at else None,
                "doctor_id": user.doctor.id
                if user.role == Role.DOCTOR.name and user.doctor
                else None,
                "patient_id": user.patient.id
                if user.role == Role.PATIENT.name and user.patient
                else None,
            }
            for user in users
        ]

        return {
            "items": result,
            "pagination": {
                "page": users_page.page,
                "limit": users_page.per_page,
                "total": users_page.total,
                "pages": users_page.pages
            }
        }, MessageCode.SUCCESS

    def get_clinics(self):
        clinics = self.admin_repo.get_all_clinics()

        result = [
            {
                "id": clinic.id,
                "name": clinic.name,
                "address": clinic.address,
                "phone": clinic.phone,
                "doctor_count": len(clinic.doctors),
                "created_at": clinic.created_at.isoformat()
                if clinic.created_at else None
            }
            for clinic in clinics
        ]

        return result, MessageCode.SUCCESS

    def get_schedules(self, page, limit, filters):
        doctor_page = self.admin_repo.get_all_schedules(
            page=page,
            limit=limit,
            filters=filters
        )

        doctors = doctor_page.items
        result = []

        for doctor in doctors:
            item = {
                "doctor_id": doctor.id,
                "doctor_name": doctor.user.full_name if doctor.user else None,
                "clinic_id": doctor.clinic_id,
                "specialties": [],
                "regular": [],
                "extra_shift": [],
                "weekend_shift": []
            }

            doctor_specialties = doctor.doctor_specialties

            if filters.get("specialty_id"):
                doctor_specialties = [
                    ds for ds in doctor_specialties
                    if ds.specialty_id == filters["specialty_id"]
                ]

            for ds in doctor_specialties:
                if ds.specialty:
                    item["specialties"].append({
                        "id": ds.specialty.id,
                        "name": ds.specialty.name
                    })

                schedules = ds.schedules or []

                for s in schedules:
                    payload = {
                        "id": s.id,
                        "doctor_specialty_id": ds.id,
                        "specialty_id": ds.specialty_id,
                        "day_of_week": s.day_of_week,
                        "start_time": str(s.start_time),
                        "end_time": str(s.end_time),
                        "status": s.status,
                        "reason": s.reason
                    }

                    if (
                            s.type == ScheduleType.REGULAR.name
                            and s.status != ScheduleStatus.LEAVE_APPROVED.name
                    ):
                        item["regular"].append(payload)

                    elif (
                            s.type == ScheduleType.EXTRA_SHIFT.name
                            and s.status != ScheduleStatus.EXTRA_REJECTED.name
                    ):
                        item["extra_shift"].append(payload)

                    elif (
                            s.type == ScheduleType.WEEKEND_SHIFT.name
                            and s.status != ScheduleStatus.WEEKEND_REJECTED.name
                    ):
                        item["weekend_shift"].append(payload)

            result.append(item)

        return {
            "items": result,
            "pagination": {
                "page": doctor_page.page,
                "limit": doctor_page.per_page,
                "total": doctor_page.total,
                "pages": doctor_page.pages
            }
        }, MessageCode.SUCCESS

    def get_payments(self, page, limit):
        payments = self.admin_repo.get_all_payment_transactions(page=page, limit=limit)

        result = [
            {
                "id": payment.id,
                "order_id": payment.order_id,
                "patient_name": payment.patient_name,
                "provider": payment.provider,
                "transaction_code": payment.transaction_code,
                "amount": float(payment.amount),
                "status": payment.status,
                "type": payment.type,
                "logs": payment.logs,
                "created_at": payment.created_at.isoformat()
                if payment.created_at else None
            }
            for payment in payments
        ]

        return result, MessageCode.SUCCESS

    def get_payment_stats(self):
        payments = self.admin_repo.get_all_payment_transactions()

        success_payments = [
            p for p in payments
            if p.status == "SUCCESS"
        ]

        pending_payments = [
            p for p in payments
            if p.status == "PENDING"
        ]

        failed_payments = [
            p for p in payments
            if p.status == "FAILED"
        ]

        total_revenue = sum(
            float(p.amount)
            for p in success_payments
        )

        result = {
            "total_revenue": total_revenue,
            "success_count": len(success_payments),
            "pending_count": len(pending_payments),
            "failed_count": len(failed_payments)
        }

        return result, MessageCode.SUCCESS

    def get_settings(self):
        result = {
            "system_name": "MediCare System",
            "support_email": "support@medicare.com",
            "phone": "19001234",
            "address": "Ho Chi Minh City",
            "timezone": "Asia/Ho_Chi_Minh"
        }

        return result, MessageCode.SUCCESS

    def get_schedule_requests(self):
        requests = self.admin_repo.get_schedule_pending_requests()

        result = []
        day_labels = [
            "Thứ 2",
            "Thứ 3",
            "Thứ 4",
            "Thứ 5",
            "Thứ 6",
            "Thứ 7",
            "Chủ nhật"
        ]

        for item in requests:
            doctor = item.doctor_specialty.doctor
            specialty = item.doctor_specialty.specialty

            result.append({
                "id": item.id,
                "doctor_name": doctor.user.full_name,
                "specialty": specialty.name,
                "type": item.type,
                "day_of_week": item.day_of_week,
                "day_label": day_labels[item.day_of_week],
                "start_time": str(item.start_time),
                "end_time": str(item.end_time),
                "reason": item.reason,
                "status": item.status
            })

        return result, MessageCode.SUCCESS

    def get_doctor_detail_to_gen_calender(self, doctor_id):
        data = self.admin_repo.get_doctor_detail_to_gen_calender(doctor_id=doctor_id)

        if not data:
            return None, MessageCode.FAIL

        return next(iter(data.values()), None), MessageCode.SUCCESS
