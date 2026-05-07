from flask_jwt_extended import get_jwt_identity

from app.infrastructure.repositories.schedule_repository_impl import ScheduleRepositoryImpl
from app.infrastructure.repositories.time_slot_repository_impl import TimeSlotRepositoryImpl
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.interfaces.mappers.schedule_mapper import ScheduleMapper
from app.interfaces.mappers.time_slot_mapper import TimeSlotMapper
from app.shared.utils.message_code import MessageCode
from app.shared.utils.role import Role


class ScheduleQueryService:

    def __init__(self, schedule_repo: ScheduleRepositoryImpl, user_repo: UserRepositoryImpl,
                 time_slot_repo: TimeSlotRepositoryImpl):
        self.schedule_repo = schedule_repo
        self.user_repo = user_repo
        self.time_slot_repo = time_slot_repo

    def get_doctor_schedules(self, start_date, end_date):
        user_id = get_jwt_identity()

        user = self.user_repo.find_by_id(id=user_id)

        if user.role != Role.DOCTOR.name:
            return None, MessageCode.UNAUTHORIZED

        schedules = self.schedule_repo.find_schedule_by_doctor_id(user_id=user_id, start_date=start_date,
                                                                  end_date=end_date)

        return schedules, MessageCode.SUCCESS

    def get_time_slot_by_schedule(self, schedule_id, doctor_specialty_id):
        time_slots = self.time_slot_repo.find_time_slots_by_schedule_id(schedule_id=schedule_id,
                                                                        doctor_specialty_id=doctor_specialty_id)

        return [TimeSlotMapper.entity_to_dict(t) for t in time_slots], MessageCode.SUCCESS

    def get_schedule_statistics_by_doctor(self):
        user_id = get_jwt_identity()
        stats = self.schedule_repo.get_schedule_statistics_by_doctor(user_id=user_id)

        return stats, MessageCode.SUCCESS

    def get_calendar_appointment(self, start_date, end_date, specialty_id=None):
        user_id = get_jwt_identity()

        time_ranges = self.time_slot_repo.get_time_ranges(user_id=user_id, start_date=start_date, end_date=end_date)
        time_slots = self.time_slot_repo.get_time_slots_appointments(user_id=user_id, start_date=start_date,
                                                                     end_date=end_date, specialty_id=specialty_id)

        return {
            "timeRanges": time_ranges,
            "timeSlots": time_slots
        }, MessageCode.SUCCESS
