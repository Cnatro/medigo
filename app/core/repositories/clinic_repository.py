from abc import abstractmethod, ABC


class ClinicRepository(ABC):
    @abstractmethod
    def get_clinics(self): pass