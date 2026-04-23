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
    def model_to_full_info_dict(doctor_m, user_m, clinic_m, spec_m, ds_m):
        """
        Mapper này gom tất cả thông tin từ các Model joined lại thành một Dictionary.
        Service sẽ nhận cái này và trả về cho Frontend.
        """
        if not doctor_m:
            return None

        return {
            # ID các thực thể
            "doctor_id": doctor_m.id,
            "specialty_id": spec_m.id,
            "clinic_id": clinic_m.id,

            # Thông tin định danh
            "doctor_name": user_m.full_name if user_m else "N/A",
            "specialty_name": spec_m.name if spec_m else "N/A",
            "clinic_name": clinic_m.name if clinic_m else "N/A",

            # Thông tin chuyên môn
            "experience_years": doctor_m.experience_years,
            "rating_avg": doctor_m.rating_avg,
            "total_reviews": doctor_m.total_reviews,

            # Thông tin tài chính
            "consultation_fee": float(ds_m.consultation_fee) if ds_m else 0
        }