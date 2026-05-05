# interfaces/controllers/appointment_controller.py
from datetime import datetime

from flask import request
from flask_jwt_extended import get_jwt_identity
from app.shared.utils.api_response import ApiResponse

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

        return ApiResponse.success(code, {
            "id": result.id,
            "time_slot_id": result.time_slot_id,
            "status": result.status
        })

    def get_history(self):
        user_id = get_jwt_identity()

        result, code = self.appointment_query_service.get_history(user_id)

        return ApiResponse.success(code, [
            {
                "id": item.id,
                "doctor_id": item.doctor_id,
                "time_slot_id": item.time_slot_id,
                "status": item.status,
                "reason": item.reason
            }
            for item in result
        ])

    def get_detail(self, appointment_id):
        result, code = self.appointment_query_service.get_detail(appointment_id)

        if not result:
            return ApiResponse.error(code)

        datetime_str = None
        if result["date"] and result["start_time"]:
            datetime_str = datetime.strftime(
                datetime.combine(result["date"], result["start_time"]),
                "%d/%m/%Y %H:%M"
            )

        return ApiResponse.success(code, {
            "id": result["id"],
            "doctor_name": result["doctor_name"],
            "specialty": result["specialty"],
            "datetime": datetime_str,
            "type": "Tại bệnh viện",
            "clinic_name": result["clinic_name"],
            "reason": result["reason"],
            "symptoms": result["reason"]
        })
