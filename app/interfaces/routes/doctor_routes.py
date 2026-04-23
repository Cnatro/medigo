from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_doctor_query_service, get_doctor_command_service
from app.interfaces.controllers.doctor_controller import DoctorController

doctor_bp = Blueprint("doctors",__name__)

@doctor_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = DoctorController(
    doctor_query_service= get_doctor_query_service(),
    doctor_command_service= get_doctor_command_service()
)

doctor_bp.route("",methods=["GET"])(controller.get_doctors)
doctor_bp.route("/<id>", methods=["GET"])(controller.get_doctor_by_id)