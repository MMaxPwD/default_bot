import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from logging import getLogger

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import FastAPI

from bot.router import router
from core.midllewares.dependency_middleware import DependencyMiddleware
from core.settings import settings
from scheduler.scheduler import scheduler

logger = getLogger()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.update.middleware(DependencyMiddleware())
    dp.include_router(router)

    await bot.delete_webhook(drop_pending_updates=True)

    # Планировщик
    scheduler.start(bot)

    # Стартуем бота
    bot_task = asyncio.create_task(dp.start_polling(bot))

    # Сохраняем в состояние
    app.state.bot = bot
    app.state.dp = dp

    logger.info("🚀 Бот начал работу.")
    yield

    logger.info("🛑 Бот закончил работу.")
    bot_task.cancel()
    try:
        await bot_task
    except asyncio.CancelledError:
        pass
    await bot.session.close()
