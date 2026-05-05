from datetime import datetime

from sqlalchemy import extract, func, case, distinct
from typing_extensions import override

from app.core.entities.schedule import Schedule
from app.core.repositories.schedule_repository import ScheduleRepository
from app.infrastructure.db import db
from app.infrastructure.models import DoctorScheduleModel, DoctorModel, UserModel, DoctorSpecialtyModel, SpecialtyModel, \
    TimeSlotModel
from app.interfaces.mappers.schedule_mapper import ScheduleMapper
from app.shared.utils.schedule_enum import ScheduleStatus


class ScheduleRepositoryImpl(ScheduleRepository):
    @override
    def create_schedule(self, schedule: Schedule):
        model = ScheduleMapper.entity_to_model(schedule)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return ScheduleMapper.model_to_entity(model)

    @override
    def schedule_exists(self, doctor_id: str, work_date):
        day_of_week = work_date.weekday()

        return db.session.query(DoctorScheduleModel).join(
            DoctorScheduleModel.doctor_specialty
        ).filter(
            DoctorScheduleModel.day_of_week == day_of_week,
            DoctorScheduleModel.status == "ACTIVE",
            DoctorScheduleModel.doctor_specialty.has(
                doctor_id=doctor_id
            )
        ).first() is not None

    @override
    def find_schedule_by_doctor_id(self, user_id, start_date, end_date):
        models = (
            db.session.query(DoctorScheduleModel, SpecialtyModel, TimeSlotModel.date)
            .join(DoctorSpecialtyModel, DoctorSpecialtyModel.id == DoctorScheduleModel.doctor_specialty_id)
            .join(DoctorModel, DoctorModel.id == DoctorSpecialtyModel.doctor_id)
            .join(UserModel, UserModel.id == DoctorModel.user_id)
            .join(SpecialtyModel, SpecialtyModel.id == DoctorSpecialtyModel.specialty_id)
            .join(TimeSlotModel, TimeSlotModel.schedule_id == DoctorScheduleModel.id)
            .filter(
                UserModel.id == user_id,
                TimeSlotModel.date >= start_date,
                TimeSlotModel.date <= end_date
            )
            .all()
        )

        return [ScheduleMapper.entity_to_dict_my_schedules(m) for m in models]

    @override
    def get_schedule_statistics_by_doctor(self, user_id):
        now = datetime.now()

        result = (
            db.session.query(
                func.count(
                    distinct(
                        case(
                            (DoctorScheduleModel.status == ScheduleStatus.ACTIVE.name, DoctorScheduleModel.id)
                        )
                    )
                ).label("regular_shift_count"),

                func.count(
                    distinct(
                        case(
                            (DoctorScheduleModel.status == ScheduleStatus.WEEKEND_APPROVED.name , DoctorScheduleModel.id)
                        )
                    )
                ).label("weekend_shift_count"),

                func.count(
                    distinct(
                        case(
                            (DoctorScheduleModel.status == ScheduleStatus.EXTRA_APPROVED.name, DoctorScheduleModel.id)
                        )
                    )
                ).label("extra_shift_count"),

                func.count(
                    distinct(
                        case(
                            (DoctorScheduleModel.status == ScheduleStatus.LEAVE_APPROVED.name, DoctorScheduleModel.id)
                        )
                    )
                ).label("leave_count")
            )
            .join(
                DoctorSpecialtyModel,
                DoctorSpecialtyModel.id == DoctorScheduleModel.doctor_specialty_id
            )
            .join(
                DoctorModel,
                DoctorModel.id == DoctorSpecialtyModel.doctor_id
            )
            .join(
                UserModel,
                UserModel.id == DoctorModel.user_id
            )
            .join(
                TimeSlotModel,
                TimeSlotModel.schedule_id == DoctorScheduleModel.id
            )
            .filter(
                UserModel.id == user_id,
                extract("month", TimeSlotModel.date) == now.month,
                extract("year", TimeSlotModel.date) == now.year
            )
            .first()
        )

        return {
            "regular_shift_count": result.regular_shift_count or 0,
            "weekend_shift_count": result.weekend_shift_count or 0,
            "extra_shift_count": result.extra_shift_count or 0,
            "leave_count": result.leave_count or 0
        }

    @override
    def find_by_id(self, id):
        model = DoctorScheduleModel.query.filter_by(id=id).first()

        if not model:
            return None

        return ScheduleMapper.model_to_entity(model)

    @override
    def update_status(self, id, data):
        model = DoctorScheduleModel.query.filter_by(id=id).first()

        if not model:
            return None

        for key, value in data.items():
            setattr(model, key, value)

        db.session.commit()
        db.session.refresh(model)

        return ScheduleMapper.model_to_entity(model)
