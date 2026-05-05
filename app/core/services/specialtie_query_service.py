from flask_jwt_extended import get_jwt_identity

from app.infrastructure.repositories.specialtie_repository_impl import SpecialtyRepositoryImpl
from app.interfaces.mappers.specialty_mapper import SpecialtyMapper
from app.shared.utils.message_code import MessageCode


class SpecialtyQueryService:
    def __init__(self, specialty_repo: SpecialtyRepositoryImpl):
        self.specialty_repo = specialty_repo

    def get_specialties(self):
        results = self.specialty_repo.get_specialties()

        if not results:
            return None, MessageCode.FAIL

        return [
            SpecialtyMapper.entity_to_dict(r)
            for r in results
        ], MessageCode.SUCCESS

    def get_specialties_by_doctor(self):
        user_id = get_jwt_identity()

        results = self.specialty_repo.get_get_specialties_by_doctor(user_id=user_id)

        return [SpecialtyMapper.entity_to_dict(e) for e in results], MessageCode.SUCCESS
