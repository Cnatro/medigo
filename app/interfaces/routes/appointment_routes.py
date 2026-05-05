from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_appointment_command_service, get_appointment_query_service
from app.interfaces.controllers.appointment_controller import AppointmentController

appointment_bp = Blueprint("appointments",__name__)

@appointment_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = AppointmentController(
    appointment_command_service= get_appointment_command_service(),
    appointment_query_service= get_appointment_query_service()
)

appointment_bp.route("/", methods=["POST"])(controller.create)
appointment_bp.route("/history", methods=["GET"])(controller.get_history)
appointment_bp.route("/<appointment_id>", methods=["GET"])(controller.get_detail)
