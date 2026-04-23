from app.core.services.specialtie_command_service import SpecialtyCommandService
from app.core.services.specialtie_query_service import SpecialtyQueryService
from app.shared.utils.api_response import ApiResponse


class SpecialtyController:

    def __init__(self, specialty_query_service: SpecialtyQueryService, specialty_command_service: SpecialtyCommandService):
        self.specialty_query_service = specialty_query_service
        self.specialty_command_service = specialty_command_service

    def get_specialties(self):
        result, code = self.specialty_query_service.get_specialties()

        if not result:
            return ApiResponse.not_found(code, result)

        return ApiResponse.success(code, result)