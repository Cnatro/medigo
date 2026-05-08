from app.infrastructure.repositories.admin_repository_impl import AdminRepositoryImpl
from app.infrastructure.repositories.schedule_repository_impl import ScheduleRepositoryImpl
from app.shared.utils.message_code import MessageCode
from app.shared.utils.schedule_enum import ScheduleStatus, ScheduleType


class AdminCommandService:
    def __init__(self, admin_repo: AdminRepositoryImpl, schedule_repo: ScheduleRepositoryImpl):
        self.admin_repo = admin_repo
        self.schedule_repo = schedule_repo

    def approve_schedule_request(self, schedule_id):
        schedule = self.schedule_repo.find_by_id(id=schedule_id)

        if not schedule:
            return None, MessageCode.FAIL

        approved_status = None

        if schedule.type == ScheduleType.EXTRA_SHIFT.name:
            approved_status = ScheduleStatus.EXTRA_APPROVED.name

        elif schedule.type == ScheduleType.WEEKEND_SHIFT.name:
            approved_status = ScheduleStatus.WEEKEND_APPROVED.name

        elif schedule.status == ScheduleStatus.LEAVE_PENDING.name:
            approved_status = ScheduleStatus.LEAVE_APPROVED.name

        else:
            return None, MessageCode.FAIL

        updated_schedule = self.schedule_repo.update_status(
            schedule_id,
            {
                "status": approved_status,
                "is_active": True
            }
        )

        if not updated_schedule:
            return None, MessageCode.FAIL

        return updated_schedule, MessageCode.SUCCESS

    def reject_schedule_request(self, schedule_id):
        schedule = self.schedule_repo.find_by_id(id=schedule_id)

        if not schedule:
            return None, MessageCode.FAIL

        rejected_status = None

        if schedule.status == ScheduleStatus.LEAVE_PENDING.value:
            rejected_status = ScheduleStatus.LEAVE_REJECTED.value


        elif schedule.status == ScheduleStatus.EXTRA_PENDING.value:
            rejected_status = ScheduleStatus.EXTRA_REJECTED.value


        elif schedule.status == ScheduleStatus.WEEKEND_PENDING.value:
            rejected_status = ScheduleStatus.WEEKEND_REJECTED.value

        else:
            return None, MessageCode.FAIL

        updated_schedule = self.schedule_repo.update_status(
            schedule_id,
            {
                "status": rejected_status,
                "is_active": False
            }
        )

        if not updated_schedule:
            return None, MessageCode.FAIL

        return updated_schedule, MessageCode.SUCCESS