from flask import request

from app.core.entities.user import User
from app.shared.utils.api_response import ApiResponse
from app.shared.utils.role import Role


class AuthController:

    def __init__(self, user_command_service, user_query_service):
        self.user_command_service = user_command_service
        self.user_query_service = user_query_service

    def register(self):
        data = request.json

        user = User(
            id=None,
            full_name=data["full_name"],
            email=data["email"],
            phone=None,
            password=data["password"],
            role=data.get("role", Role.PATIENT.name)
        )
        profile_data = data.get("profile", {})
        result, code = self.user_command_service.register(user, profile_data)

        if not result:
            return ApiResponse.error(code)

        return ApiResponse.created(code, {
            "id": result.id,
            "email": result.email,
            "full_name": result.full_name,
            "phone": result.phone,
            "role": result.role
        })

    def login(self):
        data = request.json

        data, code = self.user_query_service.login(email=data["email"], password=data["password"])

        if not data:
            return ApiResponse.error(code)

        return ApiResponse.success(code, data=data)
