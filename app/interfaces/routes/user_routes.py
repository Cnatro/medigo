from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_user_query_service
from app.interfaces.controllers.user_controller import UserController

user_bp = Blueprint("users",__name__)

@user_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = UserController(
    user_query_service= get_user_query_service()
)

user_bp.route("/me",methods=["GET"]) (controller.get_current_user)