from abc import abstractmethod, ABC


class SpecialtyRepository(ABC):
    @abstractmethod
    def get_specialties(self): pass