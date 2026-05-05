from app.core.entities.base_entity import BaseEntity


class Schedule(BaseEntity):
    def __init__(self, id, doctor_specialty_id, day_of_week,
                 start_time, end_time, type_ = "REGULAR",is_active=True, status = "ACTIVE", reason = None):
        super().__init__(id)
        self.doctor_specialty_id = doctor_specialty_id
        self.day_of_week = day_of_week
        self.start_time = start_time
        self.end_time = end_time
        self.is_active = is_active
        self.type = type_
        self.status = status
        self.reason = reason