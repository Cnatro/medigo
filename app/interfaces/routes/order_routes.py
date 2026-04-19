from flask import Blueprint, request
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_order_command_service, get_order_query_service
from app.interfaces.controllers.order_controller import OrderController

order_bp = Blueprint("orders",__name__)

@order_bp.before_request
def authenticated():
    if request.path.endswith("/momo/callback"):
        return
    verify_jwt_in_request()

controller = OrderController(
    order_command_service=get_order_command_service(),
    order_query_service=get_order_query_service()
)

order_bp.route("",methods=["POST"])(controller.created_order)
order_bp.route("/momo/callback",methods=["POST"])(controller.momo_call_back)
order_bp.route("/cancel-order",methods=["POST"])(controller.cancel_order)