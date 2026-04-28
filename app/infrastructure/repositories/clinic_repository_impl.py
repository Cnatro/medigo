from typing_extensions import override

from app.core.repositories.clinic_repository import ClinicRepository
from app.infrastructure.db import db
from app.infrastructure.models import ClinicModel, DoctorModel
from app.interfaces.mappers.clinic_mapper import ClinicMapper


class ClinicRepositoryImpl(ClinicRepository):

    @override
    def get_clinics(self):
        subquery = db.session.query(DoctorModel.clinic_id).distinct()

        models = ClinicModel.query.filter(
            ClinicModel.id.in_(subquery)
        ).all()

        return [
            ClinicMapper.model_to_entity(m)
            for m in models
        ]
