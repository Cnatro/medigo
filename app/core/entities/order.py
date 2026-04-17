from app.core.entities.base_entity import BaseEntity


class Order(BaseEntity):

    def __init__(self, id, patient_id, appointment_id, total_amount,
                 status, created_at=None, updated_at=None):
        super().__init__(id)
        self.patient_id = patient_id
        self.appointment_id = appointment_id
        self.total_amount = total_amount
        self.status = status
        self.created_at = created_at
        self.updated_at = updated_at