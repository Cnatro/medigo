from app.core.repositories.time_slot_repository import TimeSlotRepository
from app.interfaces.mappers.time_slot_mapper import TimeSlotMapper


class TimeSlotQueryService:

    def __init__(self, time_slot_repo: TimeSlotRepository):
       self.time_slot_repo = time_slot_repo

    def get_schedule(self, doctor_specialty_id, start_date, end_date):
        slots = self.time_slot_repo.get_slots_by_doctor_and_date_range(doctor_specialty_id, start_date, end_date)

        schedule_by_date = {}
        for slot in slots:
            date_key = slot.date.isoformat()
            if date_key not in schedule_by_date:
                schedule_by_date[date_key] = []

            entity = TimeSlotMapper.model_to_entity(slot)
            schedule_by_date[date_key].append({
                "id": entity.id,
                "start_time": entity.start_time.strftime("%H:%M"),
                "end_time": entity.end_time.strftime("%H:%M"),
                "is_available": entity.is_available
            })

        return schedule_by_date