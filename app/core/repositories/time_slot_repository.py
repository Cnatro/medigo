from abc import ABC, abstractmethod
from typing import List

from app.core.entities.time_slot import TimeSlot


class TimeSlotRepository(ABC):
    @abstractmethod
    def get_slots_by_doctor_and_date_range(self, doctor_specialty_id, start_date, end_date): pass

    @abstractmethod
    def create_time_slot(self, time_slots: List[TimeSlot]): pass

    @abstractmethod
    def find_time_slots_by_schedule_id(self, schedule_id, doctor_specialty_id): pass

    @abstractmethod
    def get_by_id(self, slot_id): pass

    @abstractmethod
    def mark_unavailable(self, slot_id): pass

    @abstractmethod
    def get_model_by_id(self, slot_id): pass

    @abstractmethod
    def get_time_ranges(self, user_id, start_date, end_date): pass

    @abstractmethod
    def get_time_slots_appointments(self, user_id, start_date, end_date, specialty_id=None): pass

    @abstractmethod
    def mark_available(self, slot_id): pass
