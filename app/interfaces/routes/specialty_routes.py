from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_specialty_query_service, get_specialty_command_service
from app.interfaces.controllers.specialty_controller import SpecialtyController

specialty_bp = Blueprint("specialties",__name__)

@specialty_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = SpecialtyController(
    specialty_query_service= get_specialty_query_service(),
    specialty_command_service= get_specialty_command_service()
)

specialty_bp.route("",methods=["GET"])(controller.get_specialties)