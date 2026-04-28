import logging

from flask import request

from app.core.services.doctor_command_service import DoctorCommandService
from app.core.services.doctor_query_service import DoctorQueryService
from app.shared.utils.api_response import ApiResponse

log = logging.getLogger(__name__)

class DoctorController:

    def __init__(self, doctor_command_service: DoctorCommandService, doctor_query_service: DoctorQueryService):
        self.doctor_command_service = doctor_command_service
        self.doctor_query_service = doctor_query_service


    def get_doctors(self):
        params = request.args.to_dict(flat=False)

        result, code = self.doctor_query_service.get_filter_doctors(params)

        response_data = {
            "total": result["total"],
            "page": result["page"],
            "size": result["size"]
        }

        return ApiResponse.success(code, data=result["data"],subData=response_data)

    def get_doctor_by_id(self, id):

        data, code = self.doctor_query_service.get_doctor_by_id(id=id)

        if not data:
            return ApiResponse.not_found(code, data)

        return ApiResponse.success(code, data)
