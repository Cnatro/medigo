# interfaces/controllers/appointment_controller.py

from flask import request
from flask_jwt_extended import get_jwt_identity
from app.shared.utils.api_response import ApiResponse

class AppointmentController:

    def __init__(self, appointment_command_service):
        self.appointment_command_service = appointment_command_service

    def create(self):
        data = request.json

        user_id = get_jwt_identity()

        result, code = self.appointment_command_service.create(user_id, data)

        if not result:
            return ApiResponse.error(code)

        return ApiResponse.success(code, {
            "id": result.id,
            "time_slot_id": result.time_slot_id,
            "status": result.status
        })