from app.core.entities.order import Order
from app.core.services.payment.momo_service import MomoService
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.payment_history_repository_impl import PaymentHistoryRepositoryImpl
from app.shared.utils.appointment_enum import AppointmentStatus
from app.shared.utils.message_code import MessageCode
from app.shared.utils.payment_enum import PaymentType


class OrderCommandService:

    def __init__(self, order_repo: OrderRepositoryImpl, appointment_repo: AppointmentRepositoryImpl,
                 momo_service: MomoService, payment_repo: PaymentHistoryRepositoryImpl):
        self.order_repo = order_repo
        self.momo_service = momo_service
        self.appointment_repo = appointment_repo
        self.payment_repo = payment_repo

    def create_order(self, order: Order, data):
        order = self.order_repo.save(order)

        if not order:
            return None, MessageCode.FAIL

        momo_result = self.momo_service.created_payment(order, PaymentType.PAYMENT, data)

        if not momo_result:
            return None, MessageCode.PAYMENT_FAILED

        return {
            "order": {
                "id": order.id,
                "status": order.status,
                "total_amount": order.total_amount
            },
            "payment": momo_result
        }

    def momo_call_back(self, data):
        order, message = self.momo_service.handle_momo_callback(self.order_repo, data)
        return order, message

    def refund_money_order(self, data):
        # cancel appointment
        self.appointment_repo.update_status(appointment_id=data["appointment_id"], status=AppointmentStatus.CANCELLED.name,
                                            symptom='')
        payment_history = self.payment_repo.find_by_appointment_id(appointment_id=data["appointment_id"])

        if not payment_history:
            return None, MessageCode.SUCCESS

        result, code = self.momo_service.refund_money(self.order_repo, payment_history = payment_history)

        return result, code
