from abc import ABC, abstractmethod

from app.core.entities.doctor import Doctor


class DoctorRepository(ABC):

    @abstractmethod
    def save(self, doctor: Doctor): pass

    @abstractmethod
    def find_by_user_id(self, user_id): pass

    @abstractmethod
    def find_doctor_by_filter(self, params): pass

    @abstractmethod
    def get_doctor_profile_for_service(self, doctor_id): pass

    @abstractmethod
    def update_doctor_by_user_id(self, user_id, data): pass
