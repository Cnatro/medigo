from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_schedule_command_service, get_schedule_query_service
from app.interfaces.controllers.schedule_controller import ScheduleController

schedule_bp = Blueprint("schedules",__name__)

@schedule_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller: ScheduleController = ScheduleController(
    schedule_command_service= get_schedule_command_service(),
    schedule_query_service=get_schedule_query_service()
)

schedule_bp.route("/generate-schedule", methods=["GET"])(controller.generate_next_week_schedule)
schedule_bp.route("/my-schedules", methods=["GET"])(controller.get_doctor_schedules)
schedule_bp.route("/<id>/time-slots", methods=["GET"])(controller.get_time_slot_by_schedule)
schedule_bp.route("/stats", methods=["GET"])(controller.get_schedule_statistics_by_doctor)
schedule_bp.route("/leave", methods=["PATCH"])(controller.update_leave_schedule)
schedule_bp.route("/extra-shift/register", methods=["POST"])(controller.register_extra_shift)
schedule_bp.route("/weekend-shift/register", methods=["POST"])(controller.register_weekend_shift)
