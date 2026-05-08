from app.core.entities.time_slot import TimeSlot
from app.infrastructure.models import TimeSlotModel


class TimeSlotMapper:
    @staticmethod
    def model_to_entity(model):
        # is_busy = (
        #         model.appointment is not None and
        #         model.appointment.status in ["PENDING", "CONFIRMED"]
        # )
        return TimeSlot(
            id=model.id,
            doctor_specialty_id=model.doctor_specialty_id,
            schedule_id=model.schedule_id,
            date=model.date,
            start_time=model.start_time,
            end_time=model.end_time,
            is_available=model.is_available
        )

    # @staticmethod
    # def model_to_entity(model: TimeSlotModel):
    #     is_available = True
    #
    #     if model.appointment and model.appointment.status in ["PENDING", "CONFIRMED"]:
    #         is_available = False
    #
    #     return TimeSlot(
    #         id=model.id,
    #         doctor_id=model.doctor_id,
    #         schedule_id=model.schedule_id,
    #         date=model.date,
    #         start_time=model.start_time,
    #         end_time=model.end_time,
    #         is_available=is_available
    #     )

    @staticmethod
    def entity_to_model(entity):
        if not entity:
            return None
        return TimeSlotModel(
            id=entity.id,
            doctor_specialty_id=entity.doctor_specialty_id,
            schedule_id=entity.schedule_id,
            date=entity.date,
            start_time=entity.start_time,
            end_time=entity.end_time,
            is_available=entity.is_available
        )

    @staticmethod
    def entity_to_dict(entity):
        if not entity:
            return None

        return {
            "id": entity.id,
            "doctor_specialty_id": entity.doctor_specialty_id,
            "schedule_id": entity.schedule_id,
            "date": str(entity.date) if entity.date else None,
            "start_time": str(entity.start_time) if entity.start_time else None,
            "end_time": str(entity.end_time) if entity.end_time else None,
            "is_available": entity.is_available
        }

    @staticmethod
    def dict_to_entity(data: dict):
        if not data:
            return None

        return TimeSlot(
            id=data.get("id"),
            doctor_specialty_id=data.get("doctor_specialty_id"),
            schedule_id=data.get("schedule_id"),
            date=data.get("date"),
            start_time=data.get("start_time"),
            end_time=data.get("end_time"),
            is_available=data.get("is_available", True)
        )

    @staticmethod
    def model_to_dict_calendar_appointment(row):
        slot, appointment, patient, user, specialty = row

        status = "available"

        if appointment:
            status = "booked"
        elif not slot.is_available:
            status = "closed"

        return {
            "id": slot.id,
            "date": slot.date.strftime("%d/%m/%Y") if slot.date else None,
            "start": slot.start_time.strftime("%H:%M") if slot.start_time else None,
            "end": slot.end_time.strftime("%H:%M") if slot.end_time else None,

            "status": status,

            "specialtyId": specialty.id if specialty else None,
            "specialtyName": specialty.name if specialty else None,

            "patient": (
                {
                    "id": patient.id,
                    "name": user.full_name
                }
                if patient and user
                else None
            )
        }
