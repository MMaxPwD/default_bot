from aiogram import Router
from aiogram.types import Message


feedback_router = Router()


# Обработчик ненужных сообщений
@feedback_router.message()
async def empty_message_handler(msg: Message) -> None:
    await msg.answer(
        text="Если вы нашли неточность, то отправьте нам письмо. "
        "Выберите пункт в меню или используйте команду /contact_us ",
        parse_mode="HTML",
    )
