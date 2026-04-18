from app.core.entities.order import Order
from app.core.services.payment.momo_service import MomoService
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.shared.utils.message_code import MessageCode


class OrderCommandService:

    def __init__(self, order_repo : OrderRepositoryImpl, momo_service : MomoService):
        self.order_repo = order_repo
        self.momo_service = momo_service

    def create_order(self, order : Order):
        result = self.momo_service.created_payment(order)

        return result, MessageCode.SUCCESS