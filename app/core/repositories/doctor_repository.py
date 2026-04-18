from abc import ABC, abstractmethod

from app.core.entities.doctor import Doctor


class DoctorRepository(ABC):

    @abstractmethod
    def save(self, doctor: Doctor): pass

    @abstractmethod
    def find_by_user_id(self, user_id): pass
