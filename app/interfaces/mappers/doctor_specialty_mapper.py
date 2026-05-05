from app.core.entities.doctor_specialty import DoctorSpecialty
from app.infrastructure.models import DoctorSpecialtyModel
from app.interfaces.mappers.doctor_mapper import DoctorMapper


class DoctorSpecialtyMapper:

    @staticmethod
    def model_to_entity(model: DoctorSpecialtyModel) -> DoctorSpecialty:
        if not model:
            return None

        return DoctorSpecialty(
            id=model.id,
            doctor_id=model.doctor_id,
            specialty_id=model.specialty_id,
            consultation_fee=float(model.consultation_fee) if model.consultation_fee is not None else 0
        )

    @staticmethod
    def entity_to_model(entity: DoctorSpecialty) -> DoctorSpecialtyModel:
        if not entity:
            return None

        return DoctorSpecialtyModel(
            id=entity.id,
            doctor_id=entity.doctor_id,
            specialty_id=entity.specialty_id,
            consultation_fee=entity.consultation_fee
        )

    @staticmethod
    def model_to_dict(model: DoctorSpecialtyModel) -> dict:
        if not model:
            return None

        return {
            "id": model.id,
            "doctor_id": model.doctor_id,
            "specialty_id": model.specialty_id,
            "consultation_fee": float(model.consultation_fee) if model.consultation_fee is not None else 0
        }

    @staticmethod
    def entity_to_dict(entity: DoctorSpecialty) -> dict:
        if not entity:
            return None

        return {
            "id": entity.id,
            "doctor_id": entity.doctor_id,
            "specialty_id": entity.specialty_id,
            "consultation_fee": float(entity.consultation_fee) if entity.consultation_fee is not None else 0
        }

    @staticmethod
    def model_with_clinic_to_dict(model_data : DoctorSpecialtyModel) -> dict:
        if not model_data:
            return None

        return {
            "id": model_data.id,
            "doctor_id": model_data.doctor_id,
            "specialty_id": model_data.specialty_id,
            "consultation_fee": float(model_data.consultation_fee) if model_data.consultation_fee is not None else 0,
            "doctor": DoctorMapper.entity_to_dict(model_data.doctor)
        }