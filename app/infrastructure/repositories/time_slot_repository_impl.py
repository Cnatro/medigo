from certifi import where
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.operators import exists

from app.core.repositories.time_slot_repository import TimeSlotRepository
from app.infrastructure.db import db
from app.infrastructure.models import TimeSlotModel, AppointmentModel, DoctorScheduleModel
from app.interfaces.mappers.time_slot_mapper import TimeSlotMapper


class TimeSlotRepositoryImpl(TimeSlotRepository):
    def get_model_by_id(self, slot_id):
        return TimeSlotModel.query \
            .options(joinedload(TimeSlotModel.doctor_specialty)) \
            .filter_by(id=slot_id).first()


    # def get_by_id(self, slot_id):
    #     model = TimeSlotModel.query.filter_by(id=slot_id).first()
    #     if not model:
    #         return None
    #
    #     return TimeSlotMapper.model_to_entity(model)
    def get_by_id(self, slot_id):
        model = TimeSlotModel.query \
            .options(
            joinedload(TimeSlotModel.appointment),
            joinedload(TimeSlotModel.doctor_specialty)
        ) \
            .filter_by(id=slot_id).first()

        if not model:
            return None

        return TimeSlotMapper.model_to_entity(model)
    # def get_busy_slots(self, doctor_id, date):
    #     result = db.session.query(TimeSlotModel) \
    #         .join(AppointmentModel, AppointmentModel.time_slot_id == TimeSlotModel.id) \
    #         .filter(
    #         TimeSlotModel.doctor_id == doctor_id,
    #         TimeSlotModel.date == date,
    #         AppointmentModel.status.in_(["PENDING", "CONFIRMED"])
    #     ) \
    #         .order_by(TimeSlotModel.start_time) \
    #         .all()
    #
    #     return result

    def get_slots_by_doctor_and_date_range(self, doctor_specialty_id, start_date, end_date):
        return (
            db.session.query(TimeSlotModel)
            .join(DoctorScheduleModel, TimeSlotModel.schedule_id == DoctorScheduleModel.id)
            .options(joinedload(TimeSlotModel.appointment))
            .filter(
                TimeSlotModel.doctor_specialty_id == doctor_specialty_id,
                TimeSlotModel.date >= start_date,
                TimeSlotModel.date <= end_date,
                DoctorScheduleModel.is_active == True
            )
            .order_by(TimeSlotModel.date, TimeSlotModel.start_time)
            .all()
        )

    def mark_unavailable(self, slot_id):
        model = TimeSlotModel.query.filter_by(id=slot_id).first()
        if not model:
            return False

        model.is_available = False
        db.session.commit()
        return True
