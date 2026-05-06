from app.core.entities.appointment import Appointment
from app.infrastructure.models import AppointmentModel


class AppointmentMapper:
    @staticmethod
    def model_to_entity(model):
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
