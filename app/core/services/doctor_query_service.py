from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.shared.utils.message_code import MessageCode


class DoctorQueryService:

    def __init__(self, doctor_repo : DoctorRepositoryImpl):
        self.doctor_repo = doctor_repo

    def get_filter_doctors(self, params):
        results = self.doctor_repo.find_doctor_by_filter(params=params)

        return list(results.values()), MessageCode.SUCCESS

    def get_doctor_by_id(self, id):
        data = self.doctor_repo.get_doctor_profile_for_service(doctor_id= id)

        if not data :
            return None, MessageCode.FAIL

        return next(iter(data.values()), None), MessageCode.SUCCESS
