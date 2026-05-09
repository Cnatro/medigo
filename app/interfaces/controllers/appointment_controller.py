# interfaces/controllers/appointment_controller.py
from datetime import datetime

from flask import request
from flask_jwt_extended import get_jwt_identity

from app.core.services.appointment_command_service import AppointmentCommandService
from app.shared.utils.api_response import ApiResponse
from app.shared.utils.message_code import MessageCode


class AppointmentController:

    def __init__(self, appointment_command_service, appointment_query_service):
        self.appointment_command_service = appointment_command_service
        self.appointment_query_service = appointment_query_service

    def create(self):
        data = request.json

        user_id = get_jwt_identity()

        result, code = self.appointment_command_service.create(user_id, data)

        if not result:
            return ApiResponse.error(code)

        return ApiResponse.success(code, data=result)

    def get_history(self):
        user_id = get_jwt_identity()

        result, code = self.appointment_query_service.get_history(user_id)

        return ApiResponse.success(code, result)

        # return ApiResponse.success(code, [
        #     {
        #         "id": item.id,
        #         "doctor_id": item.doctor_id,
        #         "time_slot_id": item.time_slot_id,
        #         "status": item.status,
        #         "reason": item.reason
        #     }
        #     for item in result
        # ])

    def get_detail(self, appointment_id):
        result, code = self.appointment_query_service.get_detail(appointment_id)

        if not result:
            return ApiResponse.error(code)

        return ApiResponse.success(code, result)

    def update_complete(self, appointment_id):
        data = request.json

        result, code = self.appointment_command_service.update_complete(appointment_id, symptom = data.get("symptom", ""))

        if not result:
            return ApiResponse.error(messageCode=MessageCode.FAIL, data=None)

        return ApiResponse.success(messageCode=code, data=result)
