from app.core.entities.review import Review
from app.infrastructure.models import ReviewModel


class ReviewMapper:

    @staticmethod
    def model_to_entity(model: ReviewModel):
        if not model:
            return None

        return Review(
            id=model.id,
            appointment_id = model.appointment_id,
            patient_id = model.patient_id,
            doctor_id = model.doctor_id,
            rating = model.rating,
            comment = model.comment,
            created_at = model.created_at
        )

    @staticmethod
    def entity_to_model(entity: Review):
        if not entity:
            return None

        return ReviewModel(
            id=entity.id,
            appointment_id=entity.appointment_id,
            patient_id=entity.patient_id,
            doctor_id=entity.doctor_id,
            rating=entity.rating,
            comment=entity.comment,
            created_at=entity.created_at
        )