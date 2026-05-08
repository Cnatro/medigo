from flask_jwt_extended import create_access_token, get_jwt_identity
from passlib.handlers.argon2 import argon2

from app.shared.utils.message_code import MessageCode
from app.shared.utils.role import Role


class UserQueryService:

    def __init__(self, repo, role_query_handlers):
        self.repo = repo
        self.role_query_handlers = role_query_handlers

    def get_by_email(self, email):
        user = self.repo.find_by_email(email=email)

        if user is None:
            return None, MessageCode.USER_NOT_FOUND

        return user, MessageCode.SUCCESS

    def login(self, email, password):
        user = self.repo.find_by_email(email=email)

        if user is None or not argon2.verify(password, user.password):
            return None, MessageCode.INVALID_CREDENTIALS

        access_token = create_access_token(identity=user.id)

        return {
            "access_token": access_token,
            "user_id": user.id,
            "email": user.email
        }, MessageCode.SUCCESS

    def get_current_user(self):
        current_user_id = get_jwt_identity()

        user = self.repo.find_by_id(id=current_user_id)

        if not user:
            return None, MessageCode.USER_NOT_FOUND

        if user.role == Role.ADMIN.name:
            return {
                "id": user.id,
                "email": user.email,
                "full_name": user.full_name,
                "role": user.role,
                "avatar_url": user.avatar_url,
                "phone": user.phone,
            }, MessageCode.SUCCESS


        handler = self.role_query_handlers.get(user.role)

        if not handler:
            return None, MessageCode.ROLE_NOT_SUPPORTED

        profile = handler.get_profile(user_id=current_user_id)

        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "avatar_url":user.avatar_url ,
            "phone":user.phone,
            "profile": profile.__dict__ if profile else None
        }, MessageCode.SUCCESS
