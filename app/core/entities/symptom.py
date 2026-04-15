from app.core.entities.base_entity import BaseEntity


class Symptom(BaseEntity):
    def __init__(self, id, name, description, embedding=None):
        super().__init__(id)
        self.name = name
        self.description = description
        self.embedding = embedding