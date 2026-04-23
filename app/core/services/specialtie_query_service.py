from app.infrastructure.repositories.specialtie_repository_impl import SpecialtyRepositoryImpl
from app.interfaces.mappers.specialty_mapper import SpecialtyMapper
from app.shared.utils.message_code import MessageCode


class SpecialtyQueryService:
    def __init__(self, specialty_repo : SpecialtyRepositoryImpl):
        self.specialty_repo = specialty_repo


    def get_specialties(self):
        results = self.specialty_repo.get_specialties()

        if not results:
            return None, MessageCode.FAIL

        return [
            SpecialtyMapper.entity_to_dict(r)
            for r in results
        ], MessageCode.SUCCESS