from app.shared.utils.api_response import ApiResponse


class UserController:

    def __init__(self, user_query_service):
        self.user_query_service = user_query_service

    def get_current_user(self):
        data, code = self.user_query_service.get_current_user()

        if not data:
            return ApiResponse.error(code), 401

        return ApiResponse.success(messageCode=code, data=data)
