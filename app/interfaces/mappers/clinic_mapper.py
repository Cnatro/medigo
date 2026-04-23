from app.core.entities.clinic import Clinic
from app.infrastructure.models.clinic_model import ClinicModel


class ClinicMapper:

    @staticmethod
    def model_to_entity(model: ClinicModel) -> Clinic:
        if not model:
            return None

        return Clinic(
            id=model.id,
            name=model.name,
            address=model.address,
            phone=model.phone,
            latitude=model.latitude,
            longitude=model.longitude,
            created_at=model.created_at
        )

    @staticmethod
    def entity_to_model(entity: Clinic) -> ClinicModel:
        if not entity:
            return None

        return ClinicModel(
            id=entity.id,
            name=entity.name,
            address=entity.address,
            phone=entity.phone,
            latitude=entity.latitude,
            longitude=entity.longitude,
            created_at=entity.created_at
        )

    @staticmethod
    def model_to_dict(model: ClinicModel) -> dict:
        if not model:
            return None

        return {
            "id": model.id,
            "name": model.name,
            "address": model.address,
            "phone": model.phone,
            "latitude": model.latitude,
            "longitude": model.longitude,
            "created_at": model.created_at.isoformat() if model.created_at else None
        }

    @staticmethod
    def entity_to_dict(entity: Clinic) -> dict:
        if not entity:
            return None

        return {
            "id": entity.id,
            "name": entity.name,
            "address": entity.address,
            "phone": entity.phone,
            "latitude": entity.latitude,
            "longitude": entity.longitude,
            "created_at": entity.created_at.isoformat() if entity.created_at else None
        }