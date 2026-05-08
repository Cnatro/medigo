from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.shared.utils.message_code import MessageCode


class DoctorQueryService:

    def __init__(self, doctor_repo: DoctorRepositoryImpl):
        self.doctor_repo = doctor_repo

    def get_filter_doctors(self, params):
        result = self.doctor_repo.find_doctor_by_filter(params=params)

        return result, MessageCode.SUCCESS

    def get_doctor_by_id(self, id):
        data = self.doctor_repo.get_doctor_profile_for_service(doctor_id=id)

        if not data:
            return None, MessageCode.FAIL

        return next(iter(data.values()), None), MessageCode.SUCCESS

    def get_appointments_by_status(self, id, data):
        results = self.doctor_repo.get_appointments_by_status(id=id, data=data)

        data = [{
            "id": appointment.id,
            "patientId": appointment.patient_id,
            "name": appointment.patient.user.full_name,
            "phone": appointment.patient.user.phone,
            "gender": appointment.patient.gender,
            "examDate": appointment.time_slot.date.strftime("%Y-%m-%d"),
            "status": appointment.status
        } for appointment in results]

        return data, MessageCode.SUCCESS
