import uuid, logging
from flask import request

from app.core.entities.order import Order
from app.core.services.order_command_service import OrderCommandService
from app.core.services.order_query_service import OrderQueryService
from app.shared.utils.api_response import ApiResponse


log = logging.getLogger(__name__)

class OrderController:

    def __init__(self, order_command_service : OrderCommandService, order_query_service : OrderQueryService):
        self.order_command_service = order_command_service
        self.order_query_service = order_query_service


    def created_order(self):
        data = request.json

        order = Order(
            id=str(uuid.uuid4()),
            patient_id="d1b82e2d-35e0-4434-a258-935e5724ad0c",
            appointment_id="c43308d2-77ce-4cd2-a746-65c456999533",
            total_amount=20000,  # tiền test
            status="PENDING"
        )

        result , code = self.order_command_service.create_order(order)

        return ApiResponse.created(code, result)

    def momo_call_back(self):
        data = request.json

        log.info("MOMO call back: %s", data)
        result, code = self.order_command_service.momo_call_back(data)
        log.info("MOMO call back result: %s", result)
        return ApiResponse.success(code, result)


    def cancel_order(self):
        result , code = self.order_command_service.refund_money_order()

        return ApiResponse.success(code, result)