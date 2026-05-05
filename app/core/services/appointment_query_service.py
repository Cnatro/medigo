from app.infrastructure.repositories.appointment_repository_impl import AppointmentRepositoryImpl
from app.shared.utils.message_code import MessageCode


class AppointmentQueryService:

    def __init__(self, appointment_repo: AppointmentRepositoryImpl):
        self.appointment_repo = appointment_repo

    def get_history(self, user_id):
        data = self.appointment_repo.get_history_by_patient(user_id)

        if not data:
            return [], MessageCode.SUCCESS

        return data, MessageCode.SUCCESS


    def get_detail(self, appointment_id):
        data = self.appointment_repo.get_detail(appointment_id)

        if not data:
            return None, MessageCode.FAIL

        return data, MessageCode.SUCCESS