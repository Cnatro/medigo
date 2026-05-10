from app.core.entities.appointment import Appointment
from app.infrastructure.models import AppointmentModel


class AppointmentMapper:
    @staticmethod
    def model_to_entity(model):
        return Appointment(
            id=model.id,
            doctor_id=model.doctor_id,
            doctor_specialty_id=model.doctor_specialty_id,
            patient_id=model.patient_id,
            time_slot_id=model.time_slot_id,
            reason=model.reason,
            status=model.status,
            symptom=model.symptom,
        )

    @staticmethod
    def entity_to_model(entity):
        return AppointmentModel(
            patient_id=entity.patient_id,
            doctor_id=entity.doctor_id,
            time_slot_id=entity.time_slot_id,
            doctor_specialty_id=entity.doctor_specialty_id,
            status=entity.status,
            reason=entity.reason,
            symptom=entity.symptom
        )

    @staticmethod
    def model_to_detail(model):
        doctor = model.doctor
        user = doctor.user if doctor else None
        clinic = doctor.clinic if doctor else None
        slot = model.time_slot
        specialty_rel = model.doctor_specialty
        patient = model.patient
        patient_user = patient.user if patient else None

        return {
            "id": model.id,
            "reason": model.reason,
            "status": model.status,
            "symptom": model.symptom,

            "date": slot.date if slot else None,
            "start_time": slot.start_time if slot else None,
            "end_time": slot.end_time if slot else None,

            # "has_reviewed": model.review is not None,

            "doctor": {
                "id": doctor.id if doctor else None,
                "full_name": user.full_name if user else None,
                "avatar": user.avatar_url if user else None,
                "bio": doctor.bio if doctor else None,
                "experience_years": doctor.experience_years if doctor else None,
                "rating_avg": doctor.rating_avg if doctor else 0,
                "total_reviews": doctor.total_reviews if doctor else 0
            } if doctor else None,

            "specialty": {
                "id": specialty_rel.specialty.id if specialty_rel and specialty_rel.specialty else None,
                "name": specialty_rel.specialty.name if specialty_rel and specialty_rel.specialty else None,
                "fee": str(specialty_rel.consultation_fee) if specialty_rel else None
            } if specialty_rel else None,

            "clinic": {
                "id": clinic.id if clinic else None,
                "name": clinic.name if clinic else None,
                "address": clinic.address if clinic else None,
                "phone": clinic.phone if clinic else None
            } if clinic else None,

            "patient": {
                "id": patient.id if patient else None,
                "full_name": patient_user.full_name if patient_user else None,
                "avatar": patient_user.avatar_url if patient_user else None,
                "phone": patient_user.phone if patient_user else None,
                "email": patient_user.email if patient_user else None,
                "gender": patient.gender if patient else None,
                "dob": patient.date_of_birth.strftime("%Y-%m-%d") if patient and patient.date_of_birth else None
            } if patient else None,
        }

    @staticmethod
    def model_to_history(model):
        doctor = model.doctor
        doctor_user = doctor.user if doctor else None
        clinic = doctor.clinic if doctor else None

        specialty_rel = model.doctor_specialty
        specialty = specialty_rel.specialty if specialty_rel else None

        slot = model.time_slot

        return {
            "id": model.id,
            "status": model.status,
            "reason": model.reason,
            "symptom": model.symptom,

            "has_reviewed": model.review is not None,

            "doctor": {
                "id": doctor.id if doctor else None,
                "full_name": doctor_user.full_name if doctor_user else None,
            },

            "specialty": {
                "id": specialty.id if specialty else None,
                "name": specialty.name if specialty else None,
            },

            "clinic": {
                "id": clinic.id if clinic else None,
                "name": clinic.name if clinic else None,
                "address": clinic.address if clinic else None,
            },

            "schedule": {
                "date": slot.date.strftime("%Y-%m-%d") if slot and slot.date else None,
                "start_time": str(slot.start_time) if slot else None,
                "end_time": str(slot.end_time) if slot else None,
            }
        }