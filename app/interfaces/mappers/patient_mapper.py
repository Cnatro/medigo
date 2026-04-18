from app.core.entities.patient import Patient
from app.infrastructure.models import PatientModel


class PatientMapper:

    @staticmethod
    def model_to_entity(model):
        if not model:
            return None

        return Patient(
            id=model.id,
            user_id=model.user_id,
            date_of_birth=model.date_of_birth,
            gender=model.gender,
            created_at=model.created_at
        )

    @staticmethod
    def entity_to_model(entity):
        if not entity:
            return None

        return PatientModel(
            id=entity.id,
            user_id=entity.user_id,
            date_of_birth=entity.date_of_birth,
            gender=entity.gender
        )