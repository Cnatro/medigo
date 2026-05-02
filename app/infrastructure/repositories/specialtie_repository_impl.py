from typing import override

from app.core.repositories.specialtie_repository import SpecialtyRepository
from app.infrastructure.db import db
from app.infrastructure.models import SpecialtyModel, DoctorSpecialtyModel
from app.interfaces.mappers.specialty_mapper import SpecialtyMapper


class SpecialtyRepositoryImpl(SpecialtyRepository):
    @override
    def get_specialties(self):
        subquery = db.session.query(DoctorSpecialtyModel.specialty_id).distinct()

        models = SpecialtyModel.query.filter(
            SpecialtyModel.id.in_(subquery)
        ).all()

        return [
            SpecialtyMapper.model_to_entity(m)
            for m in models
        ]

    @override
    def find_names_by_ids(self, ids):
        models = SpecialtyModel.query.filter(
            SpecialtyModel.id.in_(ids)
        ).all()

        return [
            SpecialtyMapper.model_to_entity(m) for m in models
        ]