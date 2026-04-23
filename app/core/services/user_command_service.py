from flask_jwt_extended import get_jwt_identity
from passlib.hash import argon2
from pyexpat.errors import messages

from app.core.entities.user import User
from app.core.services.cloudinary.cloudinary_service import CloudinaryService
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.shared.utils.message_code import MessageCode


class UserCommandService:

    def __init__(self, repo: UserRepositoryImpl, role_handlers, role_update_handlers):
        self.repo = repo
        self.role_handlers = role_handlers
        self.role_update_handlers = role_update_handlers

    def register(self, user: User, profile_data):

        if self.repo.find_by_email(user.email):
            return None, MessageCode.USER_EXISTS

        user.password = argon2.hash(user.password)
        saved_user = self.repo.save(user=user)

        handler = self.role_handlers.get(user.role)

        if not handler:
            return None, MessageCode.ROLE_NOT_SUPPORTED

        handler.handle(user=saved_user, profile=profile_data)

        return saved_user, MessageCode.REGISTER_USER_SUCCESS

    def update_profile(self, data, avatar_file=None):
        current_user_id = get_jwt_identity()
        user = self.repo.find_by_id(id=current_user_id)
        user_data = {k: data[k] for k in ["full_name", "phone"] if k in data}

        updated_user = user
        if avatar_file:
            user_data["avatar_url"] = CloudinaryService.upload_image(
                avatar_file,
                folder=f"medigo-avatar/users/{user.id}"
            )

        if user_data:
            updated_user = self.repo.update_current_user(user_id=current_user_id, data=user_data)

        handler = self.role_update_handlers.get(user.role)

        if not handler:
            return None, MessageCode.ROLE_NOT_SUPPORTED

        handler.update_user(user_id=current_user_id, data=data)

        return updated_user, MessageCode.SUCCESS
