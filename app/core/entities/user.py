from app.core.entities.base_entity import BaseEntity


class User(BaseEntity):
    def __init__(self, id, full_name, email, password, role,
                 created_at=None, updated_at=None, phone= None, avatar_url = None):
        super().__init__(id)
        self.full_name = full_name
        self.email = email
        self.phone = phone
        self.password = password
        self.role = role
        self.created_at = created_at
        self.updated_at = updated_at
        self.avatar_url = avatar_url