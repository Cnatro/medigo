from app.core.entities.appointment import Appointment
from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.infrastructure.repositories.time_slot_repository_impl import TimeSlotRepositoryImpl
from app.shared.utils.message_code import MessageCode


class AppointmentCommandService:
    def __init__(self, appointment_repo: AppointmentRepositoryImpl, time_slot_repo: TimeSlotRepositoryImpl):
        self.time_slot_repo = time_slot_repo
        self.appointment_repo = appointment_repo

    def create(self, user_id, data):

        time_slot = self.time_slot_repo.get_by_id(data["time_slot_id"])
        if not time_slot:
            return None, MessageCode.INVALID_DATA

        if not time_slot.is_available:
            return None, MessageCode.FAIL

        # if time_slot.appointment:
        #     return None, MessageCode.FAIL

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
            status="PENDING",
            reason=data.get("reason")
        )

        result = self.appointment_repo.create(user_id, appointment)


        if not result:
            print("not result")
            return None, MessageCode.FAIL

        self.time_slot_repo.mark_unavailable(data["time_slot_id"])

        return result, MessageCode.SUCCESS