import uuid
from flask import request

from app.core.entities.order import Order
from app.core.services.order_command_service import OrderCommandService
from app.core.services.order_query_service import OrderQueryService
from app.shared.utils.api_response import ApiResponse


class OrderController:

    def __init__(self, order_command_service : OrderCommandService, order_query_service : OrderQueryService):
        self.order_command_service = order_command_service
        self.order_query_service = order_query_service


    def created_order(self):
        data = request.json

        order = Order(
            id=str(uuid.uuid4()),
            patient_id="patient-123",
            appointment_id="appointment-456",
            total_amount=10000,  # tiền test
            status="PENDING"
        )

        result , code = self.order_command_service.create_order(order)

        return ApiResponse.created(code, result)

