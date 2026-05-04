from abc import ABC, abstractmethod


class TimeSlotRepository(ABC):
    @abstractmethod
    def get_slots_by_doctor_and_date_range(self, doctor_specialty_id, start_date, end_date): pass

    @abstractmethod
    def get_by_id(self, slot_id): pass

    @abstractmethod
    def mark_unavailable(self, slot_id): pass

    @abstractmethod
    def get_model_by_id(self, slot_id): pass