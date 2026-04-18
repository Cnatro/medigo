from app.core.entities.doctor import Doctor
from app.infrastructure.models import DoctorModel


class DoctorMapper:

    @staticmethod
    def model_to_entity(model: DoctorModel):
        if not model:
            return None

        return Doctor(
            id=model.id,
            user_id=model.user_id,
            bio=model.bio,
            experience_years=model.experience_years,
            clinic_id=model.clinic_id,
            rating_avg=model.rating_avg,
            total_reviews=model.total_reviews,
            embedding=model.embedding,
            created_at=model.created_at
        )

    @staticmethod
    def entity_to_model(entity: Doctor):
        if not entity:
            return None

        return DoctorModel(
            id=entity.id,
            user_id=entity.user_id,
            bio=entity.bio,
            experience_years=entity.experience_years,
            clinic_id=entity.clinic_id,
            rating_avg=entity.rating_avg,
            total_reviews=entity.total_reviews,
            embedding=entity.embedding
        )
