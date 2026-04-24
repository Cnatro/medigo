from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_doctor_query_service, get_doctor_command_service, get_time_slot_query_service
from app.interfaces.controllers.doctor_controller import DoctorController
from app.interfaces.controllers.time_slot_controller import TimeSlotController

time_slot_bp = Blueprint("time_slots",__name__)

@time_slot_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller: TimeSlotController = TimeSlotController(
    time_slot_query_service= get_time_slot_query_service(),
)

time_slot_bp.route("/<doctor_id>/slots", methods=["GET"])(controller.get_slots)