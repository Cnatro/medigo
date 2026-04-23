from app.infrastructure.repositories.clinic_repository_impl import ClinicRepositoryImpl
from app.interfaces.mappers.clinic_mapper import ClinicMapper
from app.shared.utils.message_code import MessageCode


class ClinicQueryService:
    def __init__(self, clinic_repo : ClinicRepositoryImpl):
        self.clinic_repo = clinic_repo


    def get_clinics(self):
        results = self.clinic_repo.get_clinics()

        if not results:
            return None, MessageCode.FAIL

        return [
            ClinicMapper.entity_to_dict(r)
            for r in results
        ], MessageCode.SUCCESS