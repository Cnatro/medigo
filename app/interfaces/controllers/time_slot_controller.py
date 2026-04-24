import logging
from datetime import datetime

from flask import request

from app.core.services.time_slot_query_service import TimeSlotQueryService
from app.interfaces.routes.doctor_routes import doctor_bp
from app.shared.utils.api_response import ApiResponse
from app.shared.utils.message_code import MessageCode

log = logging.getLogger(__name__)

class TimeSlotController:
    def __init__(self, time_slot_query_service: TimeSlotQueryService):
        self.time_slot_query_service = time_slot_query_service

    def get_slots(self, doctor_id):
        start_date_str = request.args.get("start_date")
        end_date_str = request.args.get("end_date")

        if not start_date_str or not end_date_str:
            return ApiResponse.error(MessageCode.INVALID_DATA)

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            return ApiResponse.error(MessageCode.INVALID_DATA)

        data = self.time_slot_query_service.get_schedule(doctor_id, start_date, end_date)

        return ApiResponse.success(MessageCode.SUCCESS, data)