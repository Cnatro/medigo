from app.core.services.admin_command_service import AdminCommandService
from app.core.services.admin_query_service import AdminQueryService
from app.shared.utils.api_response import ApiResponse


class AdminController:

    def __init__(self, admin_query_service: AdminQueryService, admin_command_service: AdminCommandService):
        self.admin_query_service = admin_query_service
        self.admin_command_service = admin_command_service

    def get_dashboard_stats(self):
        result, code = self.admin_query_service.get_dashboard_stats()
        return ApiResponse.success(code, result)

    def get_weekly_appointments(self):
        result, code = self.admin_query_service.get_weekly_appointments()
        return ApiResponse.success(code, result)

    def get_top_doctors(self):
        result, code = self.admin_query_service.get_top_doctors()
        return ApiResponse.success(code, result)

    def get_recent_appointments(self):
        result, code = self.admin_query_service.get_recent_appointments()
        return ApiResponse.success(code, result)

    def get_dashboard_overview(self):
        result, code = self.admin_query_service.get_dashboard_overview()
        return ApiResponse.success(code, result)

    def get_users(self):
        result, code = self.admin_query_service.get_users()
        return ApiResponse.success(code, result)

    def get_clinics(self):
        result, code = self.admin_query_service.get_clinics()
        return ApiResponse.success(code, result)

    def get_schedules(self):
        result, code = self.admin_query_service.get_schedules()
        return ApiResponse.success(code, result)

    def get_payments(self):
        result, code = self.admin_query_service.get_payments()
        return ApiResponse.success(code, result)

    def get_payment_stats(self):
        result, code = self.admin_query_service.get_payment_stats()
        return ApiResponse.success(code, result)

    def get_settings(self):
        result, code = self.admin_query_service.get_settings()
        return ApiResponse.success(code, result)

    def get_schedule_requests(self):
        result, code = self.admin_query_service.get_schedule_requests()
        return ApiResponse.success(code, result)

    def approve_schedule_request(self, schedule_id):
        result, code = self.admin_command_service.approve_schedule_request(
            schedule_id
        )
        return ApiResponse.success(code, result)

    def reject_schedule_request(self, schedule_id):
        result, code = self.admin_command_service.reject_schedule_request(
            schedule_id
        )
        return ApiResponse.success(code, result)
