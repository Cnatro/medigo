from typing_extensions import override

from app.core.entities.doctor import Doctor
from app.core.repositories.doctor_repository import DoctorRepository
from app.core.services.filter.doctor_filter import DoctorFilter
from app.infrastructure.db import db
from app.infrastructure.models import DoctorModel, ClinicModel, ReviewModel, SpecialtyModel, DoctorSpecialtyModel, \
    UserModel
from app.interfaces.mappers.doctor_mapper import DoctorMapper
from sqlalchemy import case


class DoctorRepositoryImpl(DoctorRepository):

    def get_doctor_profile_for_service(self, doctor_id):
        result = db.session.query(
            DoctorModel, UserModel, ClinicModel, SpecialtyModel, DoctorSpecialtyModel
        ).join(UserModel, UserModel.id == DoctorModel.user_id) \
            .join(ClinicModel, ClinicModel.id == DoctorModel.clinic_id) \
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.doctor_id == DoctorModel.id) \
            .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id) \
            .filter(DoctorModel.id == doctor_id) \
            .all()

        if not result:
            return None

        return DoctorMapper.map_doctors(result)

    @override
    def find_doctor_by_filter(self, params):

        base_query = db.session.query(
            DoctorModel.id
        ).join(UserModel, UserModel.id == DoctorModel.user_id) \
            .join(ClinicModel, ClinicModel.id == DoctorModel.clinic_id) \
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.doctor_id == DoctorModel.id) \
            .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id)

        filter_obj = DoctorFilter(base_query, params)
        query = filter_obj.apply()

        page, size, offset = filter_obj.apply_pagination()

        doctor_cte = query \
            .order_by(None)\
            .with_entities(DoctorModel.id) \
            .distinct() \
            .offset(offset) \
            .limit(size) \
            .cte("doctor_pagination")

        total = query.order_by(None).with_entities(DoctorModel.id).distinct().count()

        final_query = db.session.query(
            DoctorModel,
            UserModel,
            ClinicModel,
            SpecialtyModel,
            DoctorSpecialtyModel
        ).join(UserModel, UserModel.id == DoctorModel.user_id) \
            .join(ClinicModel, ClinicModel.id == DoctorModel.clinic_id) \
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.doctor_id == DoctorModel.id) \
            .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id) \
            .join(doctor_cte, doctor_cte.c.id == DoctorModel.id)

        ordering_ids = [row[0] for row in db.session.query(doctor_cte.c.id).all()]

        ordering = case(
            {id: index for index, id in enumerate(ordering_ids)},
            value=DoctorModel.id
        )

        final_query = final_query.order_by(ordering)

        results = final_query.all()

        mapped = DoctorMapper.map_doctors(results)

        return {
            "data": list(mapped.values()),
            "total": total,
            "page": page,
            "size": size
        }

    @override
    def save(self, doctor: Doctor):
        model = DoctorMapper.entity_to_model(doctor)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return DoctorMapper.model_to_entity(model)

    @override
    def find_by_user_id(self, user_id):
        model = DoctorModel.query.filter_by(user_id=user_id).first()

        if not model:
            return None

        return DoctorMapper.model_to_entity(model)

    @override
    def update_doctor_by_user_id(self, user_id, data):
        model = DoctorModel.query.filter_by(user_id=user_id).first()

        if not model:
            return None

        for key, value in data.items():
            setattr(model, key, value)

        db.session.commit()
        db.session.refresh(model)

        return DoctorMapper.mgodel_to_entity(model)
