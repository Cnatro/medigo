from typing import override

from app.core.repositories.specialtie_repository import SpecialtyRepository
from app.infrastructure.models import SpecialtyModel
from app.interfaces.mappers.specialty_mapper import SpecialtyMapper


class SpecialtyRepositoryImpl(SpecialtyRepository):
    @override
    def get_specialties(self):
        models = SpecialtyModel.query.all()

        return [
            SpecialtyMapper.model_to_entity(m)
            for m in models
        ]