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
            doctor_id = model.doctor_id,
            schedule_id = model.schedule_id,
            date = model.date,
            start_time = model.start_time,
            end_time = model.end_time,
            is_available = model.is_available
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
        doctor_id = entity.doctor_id,
        schedule_id = entity.schedule_id,
        date = entity.date,
        start_time = entity.start_time,
        end_time = entity.end_time,
        is_available = entity.is_available
        )

