import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.services.schedule_command_service import ScheduleCommandService

log = logging.getLogger(__name__)

class CronJobSchedule:

    def __init__(self, schedule_command_service: ScheduleCommandService):
        self.schedule_command_service = schedule_command_service

    def start_scheduler(self):
        scheduler = BackgroundScheduler()

        scheduler.add_job(
            func=self.schedule_command_service.generate_next_week_schedule,
            trigger=CronTrigger(day_of_week='sun', hour=0, minute=0),
            # trigger=CronTrigger(hour=10, minute=40),
            id='generate_next_week_schedule',
            replace_existing=True
        )

        scheduler.start()


