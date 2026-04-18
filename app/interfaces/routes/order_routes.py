from flask import Blueprint
from flask_jwt_extended import verify_jwt_in_request

from app.dependencies import get_order_command_service, get_order_query_service
from app.interfaces.controllers.order_controller import OrderController

order_bp = Blueprint("orders",__name__)

@order_bp.before_request
def authenticated():
    verify_jwt_in_request()

controller = OrderController(
    order_command_service=get_order_command_service(),
    order_query_service=get_order_query_service()
)

order_bp.route("",methods=["POST"])(controller.created_order)