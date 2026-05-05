from select import select
from sqlalchemy.orm import joinedload
from typing_extensions import override

from app.core.entities.doctor import Doctor
from app.core.entities.doctor_specialty import DoctorSpecialty
from app.core.repositories.doctor_repository import DoctorRepository
from app.core.services.filter.doctor_filter import DoctorFilter
from app.infrastructure.db import db
from app.infrastructure.models import DoctorModel, ClinicModel, ReviewModel, SpecialtyModel, DoctorSpecialtyModel, \
    UserModel
from app.interfaces.mappers.doctor_mapper import DoctorMapper
from sqlalchemy import case, text, distinct

from app.interfaces.mappers.doctor_specialty_mapper import DoctorSpecialtyMapper


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
            .order_by(None) \
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

    @override
    def find_doctors_by_specialty_ids(self, specialty_ids, limit=5):
        query = text("""
                    SELECT DISTINCT d.id,
                           u.full_name,
                           d.rating_avg,
                           d.experience_years,
                           c.name AS clinic_name
                    FROM doctors d
                    JOIN users u ON u.id = d.user_id
                    JOIN clinics c ON c.id = d.clinic_id
                    JOIN doctor_specialties ds ON ds.doctor_id = d.id
                    --JOIN time_slots ts ON ts.doctor_specialty_id = ds.id

                    WHERE ds.specialty_id = ANY(:specialty_ids)
                     --AND ts.is_available = TRUE

                    ORDER BY d.rating_avg DESC, d.experience_years DESC
                    LIMIT :limit
                """)

        result = db.session.execute(query, {
            "specialty_ids": specialty_ids,
            "limit": limit
        }).fetchall()

        return result

    @override
    def get_all_doctor_specialities(self):
        models = db.session.query(DoctorSpecialtyModel) \
            .join(DoctorModel) \
            .options(joinedload(DoctorSpecialtyModel.doctor)) \
            .all()

        return [DoctorSpecialtyMapper.model_with_clinic_to_dict(m) for m in models]

    @override
    def find_doctor_specialty_by_user_id_and_specialty_id(self,user_id, specialty_id):
        model = db.session.query(DoctorSpecialtyModel)\
            .join(DoctorModel,DoctorModel.id == DoctorSpecialtyModel.doctor_id)\
            .filter(DoctorModel.user_id == user_id, DoctorSpecialtyModel.specialty_id == specialty_id)\
            .distinct()\
            .first()

        if not model:
            return None

        return DoctorSpecialtyMapper.model_to_entity(model)

