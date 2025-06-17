from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from scheduler.tasks.send_daily_message import send_daily_message


class Scheduler:
    def __init__(self) -> None:
        self.scheduler = AsyncIOScheduler()

    def add_jobs(self, bot: Bot) -> None:
        """Добавляем все задачи (джобы) в планировщика."""
        self.scheduler.add_job(
            send_daily_message,
            trigger=CronTrigger(hour=22, minute=8),  # МСК: +3 к UTC
            args=[bot],
            id="daily_holiday_message",
            replace_existing=True,
        )

    def start(self, bot: Bot) -> None:
        """Запускаем планировщик с задачами."""
        self.add_jobs(bot)
        self.scheduler.start()

    def shutdown(self) -> None:
        """Останавливаем планировщик."""
        self.scheduler.shutdown(wait=False)


scheduler = Scheduler()
