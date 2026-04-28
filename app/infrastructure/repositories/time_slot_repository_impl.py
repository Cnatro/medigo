from certifi import where
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.operators import exists

from app.core.repositories.time_slot_repository import TimeSlotRepository
from app.infrastructure.db import db
from app.infrastructure.models import TimeSlotModel, AppointmentModel, DoctorScheduleModel


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
                DoctorScheduleModel.is_active == True
            )
            .order_by(TimeSlotModel.date, TimeSlotModel.start_time)
            .all()
        )
