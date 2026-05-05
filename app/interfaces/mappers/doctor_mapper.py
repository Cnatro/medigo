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

    @staticmethod
    def model_to_entity_find_doctor(model: DoctorModel):
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
    def entity_to_model_find_doctor(entity: Doctor):
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

    @staticmethod
    def map_doctors(rows):
        result = {}

        for doctor_m, user_m, clinic_m, spec_m, ds_m in rows:

            if doctor_m.id not in result:
                result[doctor_m.id] = {
                    "id": doctor_m.id,

                    "name": user_m.full_name if user_m else "N/A",
                    "avatar": getattr(user_m, "avatar_url", None),

                    "clinic": clinic_m.name if clinic_m else "N/A",
                    "clinic_id": clinic_m.id if clinic_m else None,
                    "clinic_address": clinic_m.address if clinic_m else None,

                    "experience": doctor_m.experience_years,
                    "rating": doctor_m.rating_avg,
                    "reviewCount": doctor_m.total_reviews,

                    "languages": [],
                    "acceptsInsurance": False,
                    "isOnline": True,

                    "specialties": []
                }

            result[doctor_m.id]["specialties"].append({
                "id": spec_m.id if spec_m else None,
                "name": spec_m.name if spec_m else "N/A",
                "price": float(ds_m.consultation_fee) if ds_m else 0,
                "doctor_specialty_id": ds_m.id
            })

        return result

    @staticmethod
    def entity_to_dict(entity: Doctor) -> dict:
        if not entity:
            return None

        return {
            "id": entity.id,
            "user_id": entity.user_id,
            "bio": entity.bio,
            "experience": entity.experience_years,
            "clinic_id": entity.clinic_id,
            "rating": entity.rating_avg,
            "reviewCount": entity.total_reviews,
            "embedding": entity.embedding,
            "created_at": entity.created_at,

            # # optional field (scheduler / API enrichment)
            # "specialties": getattr(entity, "specialties", [])
        }

    @staticmethod
    def dict_to_entity(data: dict):
        if not data:
            return None

        doctor = Doctor(
            id=data.get("id"),
            user_id=data.get("user_id"),
            bio=data.get("bio"),
            experience_years=data.get("experience"),
            clinic_id=data.get("clinic_id"),
            rating_avg=data.get("rating"),
            total_reviews=data.get("reviewCount"),
            embedding=data.get("embedding"),
            created_at=data.get("created_at"),
        )

        # # attach specialties as domain field (if your entity supports it)
        # doctor.specialties = data.get("specialties", [])

        return doctor