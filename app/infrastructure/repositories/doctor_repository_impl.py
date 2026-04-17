from typing_extensions import override

from app.core.entities.doctor import Doctor
from app.core.repositories.doctor_repository import DoctorRepository
from app.infrastructure.db import db
from app.infrastructure.models import DoctorModel
from app.interfaces.mappers.doctor_mapper import DoctorMapper


class DoctorRepositoryImpl(DoctorRepository):

    @override
    def save(self, doctor: Doctor):
        model = DoctorMapper.entity_to_model(doctor)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return DoctorMapper.model_to_entity(model)


    @override
    def find_by_user_id(self, user_id):
        model = DoctorModel.query.filter_by(user_id = user_id).first()

        if not model:
            return None

        return DoctorMapper.model_to_entity(model)