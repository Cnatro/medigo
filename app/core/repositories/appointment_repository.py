from abc import ABC, abstractmethod


class AppointmentRepository(ABC):
    @abstractmethod
    def create(self, user_id ,appointment): pass

    @abstractmethod
    def get_history_by_patient(self, user_id): pass

    @abstractmethod
    def get_detail(self, appointment_id): pass