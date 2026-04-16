from flask import Blueprint

from app.dependencies import get_user_command_service, get_user_query_service
from app.interfaces.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

controller = AuthController(
    user_command_service=get_user_command_service(),
    user_query_service=get_user_query_service()
)


auth_bp.route("/register", methods=["POST"])(controller.register)
auth_bp.route("/login", methods=["POST"])(controller.login)