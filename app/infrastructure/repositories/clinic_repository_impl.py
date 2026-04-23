from typing_extensions import override

from app.core.repositories.clinic_repository import ClinicRepository
from app.infrastructure.models import ClinicModel
from app.interfaces.mappers.clinic_mapper import ClinicMapper


class ClinicRepositoryImpl(ClinicRepository):

    @override
    def get_clinics(self):
        models = ClinicModel.query.all()

        return [
            ClinicMapper.model_to_entity(m)
            for m in models
        ]
