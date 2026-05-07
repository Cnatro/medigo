# interfaces/controllers/appointment_controller.py

from flask import request
from flask_jwt_extended import get_jwt_identity

from app.core.services.appointment_command_service import AppointmentCommandService
from app.shared.utils.api_response import ApiResponse

class AppointmentController:

    def __init__(self, appointment_command_service : AppointmentCommandService):
        self.appointment_command_service = appointment_command_service

    def create(self):
        data = request.json

        user_id = get_jwt_identity()

        result, code = self.appointment_command_service.create(user_id, data)

        if not result:
            return ApiResponse.error(code)

        return ApiResponse.created(messageCode=code, data=result)