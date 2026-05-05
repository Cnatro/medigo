from typing import List
from sqlalchemy.orm import joinedload
from typing_extensions import override

from app.core.entities.time_slot import TimeSlot
from app.core.repositories.time_slot_repository import TimeSlotRepository
from app.infrastructure.db import db
from app.infrastructure.models import TimeSlotModel, AppointmentModel, DoctorScheduleModel
from app.interfaces.mappers.time_slot_mapper import TimeSlotMapper


class TimeSlotRepositoryImpl(TimeSlotRepository):
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
                DoctorScheduleModel.is_active == True,
                DoctorScheduleModel.status == "ACTIVE"
            )
            .order_by(TimeSlotModel.date, TimeSlotModel.start_time)
            .all()
        )

    @override
    def create_time_slot(self, time_slots: List[TimeSlot]):
        if not time_slots:
            return []

        models = [
            TimeSlotMapper.entity_to_model(slot)
            for slot in time_slots
        ]

        db.session.add_all(models)
        db.session.commit()

        return [TimeSlotMapper.model_to_entity(m) for m in models]

    def find_time_slots_by_schedule_id(self, schedule_id, doctor_specialty_id):
        models = TimeSlotModel.query.filter_by(schedule_id=schedule_id, doctor_specialty_id=doctor_specialty_id,
                                               is_available=True)

        return [TimeSlotMapper.model_to_entity(m) for m in models]
