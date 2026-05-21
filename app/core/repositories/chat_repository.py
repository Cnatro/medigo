from abc import ABC, abstractmethod


class ChatRepository(ABC):

    @abstractmethod
    def create_session(self, patient_id): pass

    @abstractmethod
    def find_session_by_id(self, session_id):  pass

    @abstractmethod
    def save_message(self, session_id, sender, message): pass

    @abstractmethod
    def get_messages(self, session_id): pass

    @abstractmethod
    def get_sessions(self, patient_id): pass
