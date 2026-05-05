from typing import override

from app.core.repositories.specialtie_repository import SpecialtyRepository
from app.infrastructure.db import db
from app.infrastructure.models import SpecialtyModel, DoctorSpecialtyModel, DoctorModel
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

    @override
    def get_get_specialties_by_doctor(self, user_id):
        models = db.session.query(SpecialtyModel) \
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.specialty_id == SpecialtyModel.id) \
            .join(DoctorModel, DoctorModel.id == DoctorSpecialtyModel.doctor_id) \
            .filter(DoctorModel.user_id == user_id).distinct().all()

        return [SpecialtyMapper.model_to_entity(m) for m in models]
