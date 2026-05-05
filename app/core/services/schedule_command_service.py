import os
import uuid
from collections import defaultdict
from datetime import date, timedelta, time, datetime

from flask_jwt_extended import get_jwt_identity

from app.core.entities.schedule import Schedule
from app.core.services.time_slot_command_service import TimeSlotCommandService
from app.infrastructure.models import TimeSlotModel
from app.infrastructure.repositories.doctor_repository_impl import DoctorRepositoryImpl
from app.infrastructure.repositories.schedule_repository_impl import ScheduleRepositoryImpl
from app.interfaces.mappers.schedule_mapper import ScheduleMapper
from app.shared.utils.message_code import MessageCode
from app.shared.utils.schedule_enum import ScheduleType, ScheduleStatus


class ScheduleCommandService:

    def __init__(
            self,
            doctor_repo: DoctorRepositoryImpl,
            timeslot_command_service: TimeSlotCommandService,
            schedule_repo: ScheduleRepositoryImpl
    ):
        self.doctor_repo = doctor_repo
        self.schedule_repo = schedule_repo
        self.timeslot_command_service = timeslot_command_service

    def generate_next_week_schedule(self):

        today = date.today()
        next_monday = today + timedelta(days=(7 - today.weekday()))

        doctor_specialties = self.doctor_repo.get_all_doctor_specialities()

        if not doctor_specialties:
            return {
                "message": "No doctor specialties found",
                "generated_count": 0
            }

        doctor_pool = defaultdict(lambda: {
            "doctor": None,
            "specialties": []
        })

        for ds in doctor_specialties:
            doctor = ds["doctor"]

            key = (
                doctor["clinic_id"],
                doctor["id"]
            )

            if doctor_pool[key]["doctor"] is None:
                doctor_pool[key]["doctor"] = doctor

            doctor_pool[key]["specialties"].append(ds)

        doctors = list(doctor_pool.values())

        specialty_demand = defaultdict(
            lambda: int(os.getenv("DEFAULT_DEMAND", 5))
        )

        for ds in doctor_specialties:
            clinic_id = ds["doctor"]["clinic_id"]
            specialty_id = ds["specialty_id"]

            key = (clinic_id, specialty_id)
            specialty_demand[key] += 1

        weekly_assignments = []

        for d in doctors:
            doctor = d["doctor"]

            available_specialties = d["specialties"]

            if not available_specialties:
                continue

            best_specialty = max(
                available_specialties,
                key=lambda s: specialty_demand[
                    (
                        doctor["clinic_id"],
                        s["specialty_id"]
                    )
                ]
            )

            demand_key = (
                doctor["clinic_id"],
                best_specialty["specialty_id"]
            )

            specialty_demand[demand_key] -= 1

            weekly_assignments.append({
                "doctor": doctor,
                "doctor_specialty": best_specialty
            })

        generated_count = 0

        for assignment in weekly_assignments:

            doctor = assignment["doctor"]
            doctor_specialty = assignment["doctor_specialty"]

            for day_offset in range(5):
                work_date = next_monday + timedelta(days=day_offset)

                # avoid duplicate schedule
                if self.schedule_repo.schedule_exists(
                        doctor["id"],
                        work_date
                ):
                    continue

                schedule = self.schedule_repo.create_schedule(
                    Schedule(
                        id=str(uuid.uuid4()),
                        doctor_specialty_id=doctor_specialty["id"],
                        day_of_week=work_date.weekday(),
                        start_time=time(7, 0),
                        end_time=time(17, 0)
                    )
                )

                slot_dicts = self.timeslot_command_service.generate_slots(
                    work_date=work_date,
                    start_time=time(7, 0),
                    end_time=time(17, 0),
                    doctor_specialty_id=doctor_specialty["id"],
                    schedule_id=schedule.id
                )

                slot_models = [
                    TimeSlotModel(**slot)
                    for slot in slot_dicts
                ]

                self.timeslot_command_service.create_time_slots(
                    slot_models
                )

                generated_count += 1

        return generated_count, MessageCode.SUCCESS

    def update_leave_schedule(self, data):
        schedule = self.schedule_repo.find_by_id(id=data["schedule_id"])

        if not schedule:
            return None, MessageCode.FAIL

        schedule_updated = self.schedule_repo.update_status(id=schedule.id, data=data)

        return ScheduleMapper.model_to_dict(schedule_updated), MessageCode.SUCCESS

    def register_extra_shift(self, data):
        return self.register_extra_core(
            data=data,
            shift_type=ScheduleType.EXTRA_SHIFT.name,
            status=ScheduleStatus.EXTRA_PENDING.name,
            start_time=time(19, 0),
            end_time=time(7, 0),
            slot_generator=self.timeslot_command_service.generate_extra_shift_slots
        )

    def register_weekend_shift(self, data):
        return self.register_extra_core(
            data=data,
            shift_type=ScheduleType.WEEKEND_SHIFT.name,
            status=ScheduleStatus.WEEKEND_PENDING.name,
            start_time=time(7, 0),
            end_time=time(17, 0),
            slot_generator=self.timeslot_command_service.generate_extra_shift_slots
        )

    def register_extra_core(self, *, data, shift_type, status, start_time, end_time, slot_generator):

        user_id = get_jwt_identity()
        ds = self.doctor_repo.find_doctor_specialty_by_user_id_and_specialty_id(user_id=user_id,
                                                                                specialty_id=data["specialty_id"])

        if not ds:
            return None, MessageCode.FAIL

        work_date = datetime.strptime(data["workDate"], "%Y-%m-%d").date()
        schedule = Schedule(
            id=str(uuid.uuid4()),
            doctor_specialty_id=ds.id,
            day_of_week=work_date.weekday(),
            start_time=start_time,
            end_time=end_time,
            type_=shift_type,
            status=status
        )
        result = self.schedule_repo.create_schedule(schedule)

        slot_dicts = slot_generator(
            work_date=work_date,
            start_time=start_time,
            end_time=end_time,
            doctor_specialty_id=ds.id,
            schedule_id=result.id
        )

        slot_models = [
            TimeSlotModel(**slot)
            for slot in slot_dicts
        ]

        self.timeslot_command_service.create_time_slots(
            slot_models
        )

        return result, MessageCode.SUCCESS
