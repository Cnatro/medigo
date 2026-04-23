from typing_extensions import override

from app.core.entities.doctor import Doctor
from app.core.repositories.doctor_repository import DoctorRepository
from app.infrastructure.db import db
from app.infrastructure.models import DoctorModel, ClinicModel, ReviewModel, SpecialtyModel, DoctorSpecialtyModel, \
    UserModel
from app.interfaces.mappers.doctor_mapper import DoctorMapper


class DoctorRepositoryImpl(DoctorRepository):

    def get_doctor_profile_for_service(self, doctor_id, specialty_id):
        result = db.session.query(
            DoctorModel, UserModel, ClinicModel, SpecialtyModel, DoctorSpecialtyModel
        ).join(UserModel, UserModel.id == DoctorModel.user_id) \
            .join(ClinicModel, ClinicModel.id == DoctorModel.clinic_id) \
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.doctor_id == DoctorModel.id) \
            .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id) \
            .filter(DoctorModel.id == doctor_id) \
            .filter(SpecialtyModel.id == specialty_id) \
            .first()

        if not result:
            return None

        return DoctorMapper.model_to_full_info_dict(*result)

    @override
    def find_doctor_by_filter(self, keyword=None, sort=None, specialty=None, clinic=None, price_range=None, review=None):
        query = db.session.query(
            DoctorModel, UserModel, ClinicModel, SpecialtyModel, DoctorSpecialtyModel
        ).join(UserModel, UserModel.id == DoctorModel.user_id) \
        .join(ClinicModel, ClinicModel.id == DoctorModel.clinic_id) \
        .join(DoctorSpecialtyModel, DoctorSpecialtyModel.doctor_id == DoctorModel.id) \
        .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id)

        if keyword:
            query=query.filter(db.or_(
                UserModel.full_name.ilike(f"%{keyword}%"),
                DoctorModel.bio.ilike(f"%{keyword}%")
            ))

        if specialty:
            query=query.filter(SpecialtyModel.id == specialty)

        if clinic:
            query=query.filter(ClinicModel.id == clinic)

        # if price_range and len(price_range) == 2:
        #     query = query.filter(DoctorSpecialtyModel.consultation_fee.between(price_range[0], price_range[1]))

        if review:
            query=query.filter(DoctorModel.rating_avg >= float(review))

        if sort == "price_asc":
            query = query.order_by(DoctorSpecialtyModel.consultation_fee.asc())
        elif sort == "price_desc":
            query = query.order_by(DoctorSpecialtyModel.consultation_fee.desc())
        elif sort == "rating":
            query = query.order_by(DoctorModel.rating_avg.desc())
        else:
            query = query.order_by(DoctorModel.created_at.desc())

        results = query.all()

        return [DoctorMapper.model_to_full_info_dict(doc, user, clinic, spec, ds)
            for doc, user, clinic, spec, ds in results]


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

    @override
    def find_by_user_id(self, user_id):
        model = DoctorModel.query.filter_by(user_id = user_id).first()

        if not model:
            return None

        return DoctorMapper.model_to_entity(model)