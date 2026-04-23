from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_clinic_query_service, get_clinic_command_service
from app.interfaces.controllers.clinic_controller import ClinicController

clinic_bp = Blueprint("clinics",__name__)

@clinic_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = ClinicController(
    clinic_query_service= get_clinic_query_service(),
    clinic_command_service= get_clinic_command_service()
)

clinic_bp.route("",methods=["GET"])(controller.get_clinics)