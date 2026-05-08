from flask import request

from app.core.services.schedule_command_service import ScheduleCommandService
from app.core.services.schedule_query_service import ScheduleQueryService
from app.shared.utils.api_response import ApiResponse


class ScheduleController:

    def __init__(self, schedule_command_service: ScheduleCommandService, schedule_query_service: ScheduleQueryService):
        self.schedule_command_service = schedule_command_service
        self.schedule_query_service = schedule_query_service

    def generate_next_week_schedule(self):
        result, code = self.schedule_command_service.generate_next_week_schedule()

        return ApiResponse.success(messageCode=code, data=result)

    def get_doctor_schedules(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")

        result, code = self.schedule_query_service.get_doctor_schedules(start_date=start_date, end_date=end_date)

        return ApiResponse.success(messageCode=code, data=result)

    def get_time_slot_by_schedule(self, id):
        doctor_specialty_id = request.args.get("doctor_specialty_id")
        result, code = self.schedule_query_service.get_time_slot_by_schedule(schedule_id=id,
                                                                             doctor_specialty_id=doctor_specialty_id)

        return ApiResponse.success(messageCode=code, data=result)

    def get_schedule_statistics_by_doctor(self):
        result, code = self.schedule_query_service.get_schedule_statistics_by_doctor()

        return ApiResponse.success(messageCode=code, data=result)

    def update_leave_schedule(self):
        data = request.json

        result, code = self.schedule_command_service.update_leave_schedule(data)

        return ApiResponse.success(messageCode=code, data=result)

    def register_extra_shift(self):
        data = request.json

        result, code = self.schedule_command_service.register_extra_shift(data=data)

        return ApiResponse.success(messageCode=code, data=result)

    def register_weekend_shift(self):
        data = request.json

        result, code = self.schedule_command_service.register_weekend_shift(data=data)

        return ApiResponse.success(messageCode=code, data=result)

    def get_calendar_appointment(self):
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        specialty_id = request.args.get("specialty_id")

        results, code = self.schedule_query_service.get_calendar_appointment(start_date, end_date, specialty_id)

        return ApiResponse.success(messageCode=code, data=results)
