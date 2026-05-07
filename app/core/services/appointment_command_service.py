from app.core.entities.appointment import Appointment
from app.core.entities.order import Order
from app.core.services.order_command_service import OrderCommandService
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.time_slot_repository_impl import TimeSlotRepositoryImpl
from app.shared.utils.appointment_enum import AppointmentStatus
from app.shared.utils.message_code import MessageCode
import uuid

from app.shared.utils.payment_enum import OrderStatus


class AppointmentCommandService:
    def __init__(self, appointment_repo: AppointmentRepositoryImpl, time_slot_repo: TimeSlotRepositoryImpl,
                 order_command_service: OrderCommandService):
        self.time_slot_repo = time_slot_repo
        self.appointment_repo = appointment_repo
        self.order_command_service = order_command_service

    def create(self, user_id, data):

        time_slot = self.time_slot_repo.get_by_id(data["time_slot_id"])
        if not time_slot:
            return None, MessageCode.INVALID_DATA

        if not time_slot.is_available:
            return None, MessageCode.FAIL

        if str(time_slot.doctor_specialty_id) != str(data["doctor_specialty_id"]):
            return None, MessageCode.INVALID_DATA

        time_slot_model = self.time_slot_repo.get_model_by_id(data["time_slot_id"])

        actual_doctor_id = time_slot_model.doctor_specialty.doctor_id

        appointment = Appointment(
            id=None,
            patient_id=None,
            doctor_id=actual_doctor_id,
            time_slot_id=data["time_slot_id"],
            doctor_specialty_id=data["doctor_specialty_id"],
            status=AppointmentStatus.PENDING.name,
            reason=data.get("reason")
        )

        result = self.appointment_repo.create(user_id, appointment)

        if not result:
            print("not result")
            return None, MessageCode.FAIL

        result_data = self.order_command_service.create_order(Order(
            id=str(uuid.uuid4()),
            patient_id=result.patient_id,
            appointment_id=result.id,
            total_amount=float(data["amount"]),
            status=OrderStatus.PENDING.name
        ),
            data=data
        )

        return result_data, MessageCode.SUCCESS
