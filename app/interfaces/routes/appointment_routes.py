from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_appointment_command_service
from app.interfaces.controllers.appointment_controller import AppointmentController

appointment_bp = Blueprint("appointments",__name__)

@appointment_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = AppointmentController(
    appointment_command_service= get_appointment_command_service()
)

appointment_bp.route("", methods=["POST"])(controller.create)