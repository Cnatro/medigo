from abc import ABC, abstractmethod

from app.core.entities.schedule import Schedule


class ScheduleRepository(ABC):
    @abstractmethod
    def create_schedule(self, schedule: Schedule): pass

    @abstractmethod
    def schedule_exists(self, doctor_id: str, work_date): pass

    @abstractmethod
    def find_schedule_by_doctor_id(self, user_id,start_date,end_date): pass

    @abstractmethod
    def get_schedule_statistics_by_doctor(self, user_id): pass

    @abstractmethod
    def find_by_id(self, id): pass

    @abstractmethod
    def update_status(self, id, data): pass
