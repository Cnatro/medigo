from abc import abstractmethod, ABC


class SpecialtyRepository(ABC):
    @abstractmethod
    def get_specialties(self): pass

    @abstractmethod
    def find_names_by_ids(self, ids): pass

    @abstractmethod
    def get_get_specialties_by_doctor(self,user_id): pass