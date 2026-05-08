from flask import Blueprint, request
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_admin_query_service, get_admin_command_service
from app.interfaces.controllers.admin_controller import AdminController

admin_bp = Blueprint("admin", __name__)


@admin_bp.before_request
def authenticated():
    if request.method == "OPTIONS":
        return "", 200
    verify_jwt_in_request()


controller = AdminController(
    admin_query_service=get_admin_query_service(),
    admin_command_service=get_admin_command_service()
)

admin_bp.route("/dashboard/stats", methods=["GET"])(controller.get_dashboard_stats)

admin_bp.route("/dashboard/weekly-appointments", methods=["GET"])(controller.get_weekly_appointments)

admin_bp.route("/dashboard/top-doctors", methods=["GET"])(controller.get_top_doctors)

admin_bp.route("/dashboard/recent-appointments", methods=["GET"])(controller.get_recent_appointments)

admin_bp.route("/dashboard/overview", methods=["GET"])(controller.get_dashboard_overview)

admin_bp.route("/users", methods=["GET"])(controller.get_users)

admin_bp.route("/clinics", methods=["GET"])(controller.get_clinics)

admin_bp.route("/schedules", methods=["GET"])(controller.get_schedules)

admin_bp.route("/payments", methods=["GET"])(controller.get_payments)

admin_bp.route("/payments/stats", methods=["GET"])(controller.get_payment_stats)

admin_bp.route("/settings", methods=["GET"])(controller.get_settings)

admin_bp.route("/schedule-requests", methods=["GET"])(controller.get_schedule_requests)

admin_bp.route( "/schedule-requests/<schedule_id>/approve", methods=["PATCH"] )(controller.approve_schedule_request)

admin_bp.route( "/schedule-requests/<schedule_id>/reject", methods=["PATCH"] )(controller.reject_schedule_request)
