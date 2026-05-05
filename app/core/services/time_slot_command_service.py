from datetime import datetime, timedelta

from app.infrastructure.repositories.time_slot_repository_impl import TimeSlotRepositoryImpl


class TimeSlotCommandService:

    def __init__(self, time_slot_repo: TimeSlotRepositoryImpl):
        self.time_slot_repo = time_slot_repo

    def generate_slots(self, work_date, start_time, end_time, doctor_specialty_id, schedule_id):
        slots = []

        current = datetime.combine(work_date, start_time)
        end = datetime.combine(work_date, end_time)

        while current < end:
            slot_end = current + timedelta(hours=1)

            slots.append({
                "doctor_specialty_id": doctor_specialty_id,
                "schedule_id": schedule_id,
                "date": work_date,
                "start_time": current.time(),
                "end_time": slot_end.time(),
                "is_available": True
            })

            current = slot_end

        return slots

    def create_time_slots(self, time_slots):
        slots = self.time_slot_repo.create_time_slot(time_slots=time_slots)

        if not slots:
            return []

        return slots

    def generate_extra_shift_slots(
            self,
            work_date,
            start_time,
            end_time,
            doctor_specialty_id,
            schedule_id,
            slot_minutes=60
    ):
        slots = []

        start_dt = datetime.combine(work_date, start_time)
        end_dt = datetime.combine(work_date, end_time)

        if end_time <= start_time:
            end_dt += timedelta(days=1)

        delta = timedelta(minutes=slot_minutes)

        current = start_dt

        while current < end_dt:
            slot_end = current + delta

            # clamp không vượt quá end
            if slot_end > end_dt:
                slot_end = end_dt

            slots.append({
                "doctor_specialty_id": doctor_specialty_id,
                "schedule_id": schedule_id,
                "date": work_date,
                "start_time": current.time(),
                "end_time": slot_end.time(),
                "is_available": True
            })

            current = slot_end

        return slots
