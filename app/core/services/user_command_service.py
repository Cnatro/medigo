from passlib.hash import argon2

from app.core.entities.user import User
from app.core.services.handle_role.registry import ROLE_HANDLES
from app.shared.utils.message_code import MessageCode


class UserCommandService:

    def __init__(self, repo, role_handlers):
        self.repo = repo
        self.role_handlers = role_handlers

    def register(self,user: User,profile_data):

        if self.repo.find_by_email(user.email):
            return None, MessageCode.USER_EXITS

        user.password = argon2.hash(user.password)
        saved_user = self.repo.save(user=user)

        handler = self.role_handlers.get(user.role)

        if not handler:
            return None, MessageCode.ROLE_NOT_SUPPORTED

        handler.handle(user = saved_user, profile = profile_data)

        return saved_user, MessageCode.REGISTER_USER_SUCCESS
