from abc import ABC, abstractmethod

from app.core.entities.doctor import Doctor


class DoctorRepository(ABC):

    @abstractmethod
    def save(self, doctor: Doctor): pass

    @abstractmethod
    def find_by_user_id(self, user_id): pass

    @abstractmethod
    def find_doctor_by_filter(self, keyword, sort, specialty, hospital, price_range, review): pass

    @abstractmethod
    def get_doctor_profile_for_service(self, doctor_id, specialty_id): pass
