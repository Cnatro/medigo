from app.core.entities.specialty import Specialty
from app.infrastructure.models.specialty_model import SpecialtyModel


class SpecialtyMapper:

    @staticmethod
    def model_to_entity(model: SpecialtyModel) -> Specialty:
        if not model:
            return None

        return Specialty(
            id=model.id,
            name=model.name,
            description=model.description,
            embedding=model.embedding
        )

    @staticmethod
    def entity_to_model(entity: Specialty) -> SpecialtyModel:
        if not entity:
            return None

        return SpecialtyModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            embedding=entity.embedding
        )

    @staticmethod
    def model_to_dict(model: SpecialtyModel) -> dict:
        if not model:
            return None

        return {
            "id": model.id,
            "name": model.name,
            "description": model.description
        }

    @staticmethod
    def entity_to_dict(entity: Specialty) -> dict:
        if not entity:
            return None

        return {
            "id": entity.id,
            "name": entity.name,
            "description": entity.description,
            "embedding": entity.embedding
        }