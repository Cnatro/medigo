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

    @abstractmethod
    def find_doctors_by_specialty_ids(self, specialty_ids, limit=5): pass

    @abstractmethod
    def get_all_doctor_specialities(self): pass

    @abstractmethod
    def find_doctor_specialty_by_user_id_and_specialty_id(self, user_id, specialty_id): pass

    @abstractmethod
    def create_doctor_specialties(self, doctor, specialties_ids): pass
