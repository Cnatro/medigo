from app.infrastructure.repositories.admin_repository_impl import AdminRepositoryImpl
from app.shared.utils.message_code import MessageCode
from app.shared.utils.role import Role


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
            "top_doctors": self.admin_repo.get_top_doctors(),
            "recent_appointments": self.admin_repo.get_recent_appointments()
        }, MessageCode.SUCCESS

    def get_users(self):
        users = self.admin_repo.get_all_users()

        result = [
            {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "phone": user.phone,
                "role": user.role,
                "created_at": user.created_at.isoformat(),
                "status": "active"
                if user.created_at else None
            }
            for user in users if user.role != Role.ADMIN.name
        ]

        return result, MessageCode.SUCCESS

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

    def get_schedules(self):
        schedules = self.admin_repo.get_all_schedules()

        grouped = {}

        for s in schedules:
            ds = s.doctor_specialty
            if not ds:
                continue

            doctor = ds.doctor
            specialty = ds.specialty

            key = ds.id  # doctor_specialty_id là root group

            if key not in grouped:
                grouped[key] = {
                    "doctor_specialty_id": ds.id,
                    "doctor_name": doctor.user.full_name if doctor else None,
                    "specialty": specialty.name if specialty else None,
                    "clinic_id": doctor.clinic_id if doctor else None,

                    # 🔥 tách rõ domain
                    "regular": [],
                    "extra_shift": [],
                    "weekend_shift": []
                }

            payload = {
                "id": s.id,
                "day_of_week": s.day_of_week,
                "start_time": str(s.start_time),
                "end_time": str(s.end_time),
                "status": s.status,
                "reason": s.reason
            }

            if s.type == "REGULAR":
                grouped[key]["regular"].append(payload)
            elif s.type == "EXTRA_SHIFT":
                grouped[key]["extra_shift"].append(payload)
            elif s.type == "WEEKEND_SHIFT":
                grouped[key]["weekend_shift"].append(payload)

        return list(grouped.values()), MessageCode.SUCCESS

    def get_payments(self):
        payments = self.admin_repo.get_all_payment_transactions()

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

        for item in requests:
            doctor = item.doctor_specialty.doctor
            specialty = item.doctor_specialty.specialty

            result.append({
                "id": item.id,
                "doctor_name": doctor.user.full_name,
                "specialty": specialty.name,
                "type": item.type,
                "day_of_week": item.day_of_week,
                "start_time": str(item.start_time),
                "end_time": str(item.end_time),
                "reason": item.reason,
                "status": item.status
            })

        return result, MessageCode.SUCCESS
