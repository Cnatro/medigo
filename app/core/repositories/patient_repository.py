from abc import ABC, abstractmethod

from app.core.entities.patient import Patient


class PatientRepository(ABC):

    @abstractmethod
    def save(self, patient: Patient): pass

    @abstractmethod
    def find_by_user_id(self, user_id): pass
