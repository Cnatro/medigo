from app.core.entities.base_entity import BaseEntity


class Appointment(BaseEntity):
    def __init__(self, id, patient_id, doctor_id, time_slot_id,
                 status, reason, created_at=None):
        super().__init__(id)
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.time_slot_id = time_slot_id
        self.status = status
        self.reason = reason
        self.created_at = created_at