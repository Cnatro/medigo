from app.core.entities.base_entity import BaseEntity


class Schedule(BaseEntity):
    def __init__(self, id, doctor_id, day_of_week,
                 start_time, end_time, is_active=True):
        super().__init__(id)
        self.doctor_id = doctor_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = is_active