from app.core.entities.user import User
from app.infrastructure.models import UserModel


class UserMapper:

    @staticmethod
    def model_to_entity(model):
        return User(
            id=model.id,
            full_name=model.full_name,
            email=model.email,
            phone=model.phone,
            password=model.password,
            role=model.role,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    @staticmethod
    def entity_to_model(entity):
        if not entity:
            return None

        return UserModel(
            id=entity.id,
            full_name=entity.full_name,
            email=entity.email,
            phone=entity.phone,
            password=entity.password,
            role=entity.role
        )