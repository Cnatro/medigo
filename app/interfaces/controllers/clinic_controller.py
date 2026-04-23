import logging

from app.core.services.clinic_command_service import ClinicCommandService
from app.core.services.clinic_query_service import ClinicQueryService
from app.shared.utils.api_response import ApiResponse

log = logging.getLogger(__name__)

class ClinicController:

    def __init__(self, clinic_query_service: ClinicQueryService, clinic_command_service: ClinicCommandService):
        self.clinic_query_service = clinic_query_service
        self.clinic_command_service = clinic_command_service


    def get_clinics(self):

        result, code = self.clinic_query_service.get_clinics()

        if not result:
            return ApiResponse.not_found(code, result)

        return ApiResponse.success(code, result)