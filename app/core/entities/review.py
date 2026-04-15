from app.core.entities.base_entity import BaseEntity


class Review(BaseEntity):
    def __init__(self, id, appointment_id, patient_id,
                 doctor_id, rating, comment, created_at=None):
        super().__init__(id)
        self.appointment_id = appointment_id
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.rating = rating
        self.comment = comment
        self.created_at = created_at