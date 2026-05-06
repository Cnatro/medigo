from typing import List
from sqlalchemy import text
from sqlalchemy.orm import joinedload
from typing_extensions import override

from app.core.entities.time_slot import TimeSlot
from app.core.repositories.time_slot_repository import TimeSlotRepository
from app.infrastructure.db import db
from app.infrastructure.models import TimeSlotModel, AppointmentModel, DoctorScheduleModel, PatientModel, UserModel, \
    SpecialtyModel, DoctorSpecialtyModel, DoctorModel
from app.interfaces.mappers.time_slot_mapper import TimeSlotMapper


class TimeSlotRepositoryImpl(TimeSlotRepository):
    @override
    def get_model_by_id(self, slot_id):
        return TimeSlotModel.query \
            .options(joinedload(TimeSlotModel.doctor_specialty)) \
            .filter_by(id=slot_id).first()

    @override
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

    @override
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
    def mark_unavailable(self, slot_id):
        model = TimeSlotModel.query.filter_by(id=slot_id).first()
        if not model:
            return False

        model.is_available = False
        db.session.commit()
        return True

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

    @override
    def find_time_slots_by_schedule_id(self, schedule_id, doctor_specialty_id):
        models = TimeSlotModel.query.filter_by(schedule_id=schedule_id, doctor_specialty_id=doctor_specialty_id,
                                               is_available=True)

        return [TimeSlotMapper.model_to_entity(m) for m in models]

    @override
    def get_time_ranges(self, user_id, start_date, end_date):
        sql = text("""
               SELECT time_range
               FROM (
                   SELECT
                       TO_CHAR(ts.start_time, 'HH24:MI') AS time_range,

                       CASE
                           WHEN ts.start_time >= TIME '07:00'
                               THEN ts.start_time - TIME '00:00'
                           ELSE (ts.start_time - TIME '00:00') + INTERVAL '1 day'
                       END AS sort_time

                   FROM time_slots ts
                   JOIN doctor_schedules ds
                       ON ts.schedule_id = ds.id
                   JOIN doctor_specialties ds2
                       ON ds2.id = ds.doctor_specialty_id
                   JOIN doctors d
                       ON d.id = ds2.doctor_id

                   WHERE d.user_id = :user_id
                     AND ts.date >= :start_date
                     AND ts.date <= :end_date
                     AND ds.is_active = TRUE
                     AND ds.status IN (
                         'ACTIVE',
                         'WEEKEND_APPROVED',
                         'EXTRA_APPROVED'
                     )
               ) t
               GROUP BY time_range
               ORDER BY MIN(sort_time)
           """)

        result = db.session.execute(
            sql,
            {
                "user_id": user_id,
                "start_date": start_date,
                "end_date": end_date
            }
        ).fetchall()

        return [row.time_range for row in result]

    @override
    def get_time_slots_appointments(self, user_id, start_date, end_date, specialty_id=None):
        query = (
            db.session.query(
                TimeSlotModel,
                AppointmentModel,
                PatientModel,
                UserModel,
                SpecialtyModel
            )
            .join(
                DoctorScheduleModel,
                TimeSlotModel.schedule_id == DoctorScheduleModel.id
            )
            .join(
                DoctorSpecialtyModel,
                TimeSlotModel.doctor_specialty_id == DoctorSpecialtyModel.id
            )
            .join(
                DoctorModel,
                DoctorSpecialtyModel.doctor_id == DoctorModel.id
            )
            .join(
                SpecialtyModel,
                DoctorSpecialtyModel.specialty_id == SpecialtyModel.id
            )
            .outerjoin(
                AppointmentModel,
                AppointmentModel.time_slot_id == TimeSlotModel.id
            )
            .outerjoin(
                PatientModel,
                AppointmentModel.patient_id == PatientModel.id
            )
            .outerjoin(
                UserModel,
                PatientModel.user_id == UserModel.id
            )
            .filter(
                DoctorModel.user_id == user_id,
                TimeSlotModel.date >= start_date,
                TimeSlotModel.date <= end_date,
                DoctorScheduleModel.is_active == True,
                DoctorScheduleModel.status.in_([
                    "ACTIVE",
                    "EXTRA_APPROVED",
                    "WEEKEND_APPROVED"
                ])
            )
        )

        if specialty_id:
            query = query.filter(
                DoctorSpecialtyModel.specialty_id == specialty_id
            )

        rows = query.order_by(
            TimeSlotModel.date,
            TimeSlotModel.start_time
        ).all()

        return [
            TimeSlotMapper.model_to_dict_calendar_appointment(row)
            for row in rows
        ]

    @override
    def mark_available(self, slot_id):
        model = TimeSlotModel.query.filter_by(id=slot_id).first()
        if not model:
            return False

        model.is_available = True
        db.session.commit()
        return True