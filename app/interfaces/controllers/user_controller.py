from flask import request

from app.core.services.user_command_service import UserCommandService
from app.shared.utils.api_response import ApiResponse


class UserController:

    def __init__(self, user_query_service, user_command_service: UserCommandService):
        self.user_query_service = user_query_service
        self.user_command_service = user_command_service

    def get_current_user(self):
        data, code = self.user_query_service.get_current_user()

        if not data:
            return ApiResponse.error(code)

        return ApiResponse.success(messageCode=code, data=data)

    def update_profile(self):
        try:
            data = request.form.to_dict()
            avatar = request.files.get("avatar")

            updated_user, code = self.user_command_service.update_profile(
                data=data,
                avatar_file=avatar
            )

            if not updated_user:
                return ApiResponse.error(code, None)

            return ApiResponse.success(
                code,
                data={
                    "id": updated_user.id,
                    "full_name": updated_user.full_name,
                    "email": updated_user.email,
                    "phone": updated_user.phone,
                    "avatar_url": getattr(updated_user, "avatar_url", None),
                    "role": updated_user.role
                }
            )

        except Exception as e:
            return ApiResponse.error(str(e))
