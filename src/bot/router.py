from aiogram import Router
from bot.routers.start_router import start_router
from bot.routers.feedback_router import feedback_router
from bot.routers.payment_router import payment_router

router = Router()

router.include_router(start_router)
router.include_router(payment_router)
router.include_router(feedback_router)
# Всегда последний тот у кого обработка пустых сообщений
