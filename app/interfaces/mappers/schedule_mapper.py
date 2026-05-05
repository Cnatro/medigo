from app.core.entities.schedule import Schedule
from app.infrastructure.models import DoctorScheduleModel


class ScheduleMapper:

    @staticmethod
    def model_to_entity(model: DoctorScheduleModel) -> Schedule:
        if not model:
            return None

        return Schedule(
            id=model.id,
            doctor_specialty_id=model.doctor_specialty_id,
            day_of_week=model.day_of_week,
            start_time=model.start_time,
            end_time=model.end_time,
            type_=model.type,
            is_active=model.is_active,
            status=model.status,
            reason=model.reason
        )

    @staticmethod
    def entity_to_model(entity: Schedule) -> DoctorScheduleModel:
        if not entity:
            return None

        return DoctorScheduleModel(
            id=entity.id,
            doctor_specialty_id=entity.doctor_specialty_id,
            day_of_week=entity.day_of_week,
            start_time=entity.start_time,
            end_time=entity.end_time,
            is_active=entity.is_active,
            type=entity.type,
            status=entity.status,
            reason=entity.reason
        )

    @staticmethod
    def model_to_dict(model: DoctorScheduleModel) -> dict:
        if not model:
            return None

        return {
            "id": model.id,
            "doctor_specialty_id": model.doctor_specialty_id,
            "day_of_week": model.day_of_week,
            "start_time": model.start_time.isoformat() if model.start_time else None,
            "end_time": model.end_time.isoformat() if model.end_time else None,
            "is_active": model.is_active,
            "type": model.type,
            "status": model.status,
            "reason": model.reason
        }

    @staticmethod
    def entity_to_dict_my_schedules(model) -> dict:
        if not model:
            return None

        schedule, specialty, date = model
        day_labels = [
            "Thứ 2",
            "Thứ 3",
            "Thứ 4",
            "Thứ 5",
            "Thứ 6",
            "Thứ 7",
            "Chủ nhật"
        ]

        return {
            "id": schedule.id,
            "doctor_specialty_id": schedule.doctor_specialty_id,
            "day_of_week": schedule.day_of_week,
            'day_label': day_labels[schedule.day_of_week],
            "start_time": schedule.start_time.isoformat() if schedule.start_time else None,
            "end_time": schedule.end_time.isoformat() if schedule.end_time else None,
            "is_active": schedule.is_active,
            "type": schedule.type,
            "status": schedule.status,
            "reason": schedule.reason,
            "date": date,
            "specialty": {
                "id": specialty.id,
                "name": specialty.name
            }
        }
