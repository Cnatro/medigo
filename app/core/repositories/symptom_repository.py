from abc import ABC, abstractmethod


class SymptomRepository(ABC):

    @abstractmethod
    def map_to_specialties(self, symptom_ids): pass