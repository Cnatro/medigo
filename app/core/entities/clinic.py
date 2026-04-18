from app.core.entities.base_entity import BaseEntity


class Clinic(BaseEntity):
    def __init__(self, id, name, address, phone, latitude, longitude, created_at=None):
        super().__init__(id)
        self.name = name
        self.address = address
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude
        self.created_at = created_at