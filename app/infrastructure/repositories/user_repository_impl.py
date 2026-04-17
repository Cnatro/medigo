from typing_extensions import override

from app.core.entities.user import User
from app.core.repositories.user_repository import UserRepository
from app.infrastructure.db import db
from app.infrastructure.models import UserModel
from app.interfaces.mappers.user_mapper import UserMapper


class UserRepositoryImpl(UserRepository):

    @override
    def find_by_email(self, email):
        user_model = UserModel.query.filter_by(email=email).first()

        if not user_model:
            return None

        return UserMapper.model_to_entity(user_model)

    @override
    def save(self, user : User):
        model = UserMapper.entity_to_model(user)

        db.session.add(model)
        db.session.commit()
        db.session.refresh(model)

        return UserMapper.model_to_entity(model)

    @override
    def find_by_id(self, id):
        model = UserModel.query.filter_by(id=id).first()

        if not model:
            return None

        return UserMapper.model_to_entity(model)
