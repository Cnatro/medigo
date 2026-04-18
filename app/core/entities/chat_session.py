from app.core.entities.base_entity import BaseEntity


class ChatSession(BaseEntity):
    def __init__(self, id, patient_id, created_at=None):
        super().__init__(id)
        self.patient_id = patient_id
        self.created_at = created_at