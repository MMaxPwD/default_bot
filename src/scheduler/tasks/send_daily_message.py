from aiogram import Bot
from core.settings import settings


async def send_daily_message(bot: Bot) -> None:
    await bot.send_message(chat_id=settings.ADMIN_CHAT_ID, text="Тест", parse_mode="HTML")
