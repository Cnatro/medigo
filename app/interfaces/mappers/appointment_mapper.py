from app.core.entities.appointment import Appointment
from app.infrastructure.models import AppointmentModel


class AppointmentMapper:
    @staticmethod
    def model_to_entities(model):
        return Appointment(
            id=model.id,
            doctor_id= model.doctor_id,
            doctor_specialty_id=model.doctor_specialty_id,
            patient_id=model.patient_id,
            time_slot_id=model.time_slot_id,
            reason=model.reason,
            status=model.status
        )

    @staticmethod
    def entity_to_model(entity):
        return AppointmentModel(
            patient_id=entity.patient_id,
            doctor_id=entity.doctor_id,
            time_slot_id=entity.time_slot_id,
            doctor_specialty_id=entity.doctor_specialty_id,
            status=entity.status,
            reason=entity.reason
        )

    @staticmethod
    def model_to_detail(model):
        return {
            "id": model.id,
            "doctor_name": model.doctor.user.full_name if model.doctor and model.doctor.user else None,
            "specialty": model.doctor_specialty.specialty.name if model.doctor_specialty else None,
            "clinic_name": model.doctor.clinic.name if model.doctor and model.doctor.clinic else None,
            "date": model.time_slot.date if model.time_slot else None,
            "start_time": model.time_slot.start_time if model.time_slot else None,
            "reason": model.reason,
            "status": model.status
        }
