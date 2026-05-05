from abc import ABC, abstractmethod


class AppointmentRepository(ABC):
    @abstractmethod
    def create(self, user_id ,appointment): pass