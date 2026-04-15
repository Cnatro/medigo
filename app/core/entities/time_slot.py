from app.core.entities.base_entity import BaseEntity


class TimeSlot(BaseEntity):
    def __init__(self, id, doctor_id, schedule_id, date,
                 start_time, end_time, is_available=True):
        super().__init__(id)
        self.doctor_id = doctor_id
        self.schedule_id = schedule_id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.is_available = is_available