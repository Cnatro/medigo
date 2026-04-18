from app.core.entities.base_entity import BaseEntity


class Patient(BaseEntity):
    def __init__(self, id, user_id, date_of_birth, gender, created_at=None):
        super().__init__(id)
        self.user_id = user_id
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.created_at = created_at