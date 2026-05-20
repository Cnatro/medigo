import logging

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from app.core.services.schedule_command_service import ScheduleCommandService

log = logging.getLogger(__name__)


class CronJobSchedule:

    def __init__(self, schedule_command_service: ScheduleCommandService):
        self.schedule_command_service = schedule_command_service
        self.scheduler = BackgroundScheduler()

    def start_scheduler(self, app):
        self.scheduler.add_job(
            func=self.run_job,
            trigger=CronTrigger(day_of_week='sun', hour=0, minute=0),
            # trigger=CronTrigger(hour=11, minute=3),
            id='generate_next_week_schedule',
            replace_existing=True,
            args=[app]
        )

        self.scheduler.start()


    def run_job(self, app):
        with app.app_context():
            return self.schedule_command_service.generate_next_week_schedule()
