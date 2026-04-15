from app.core.entities.base_entity import BaseEntity


class ChatMessage(BaseEntity):
    def __init__(self, id, session_id, sender, message, created_at=None):
        super().__init__(id)
        self.session_id = session_id
        self.sender = sender
        self.message = message
        self.created_at = created_at