from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from bot.keyboard.start import start_reply_kb
from services.user_service import UsersService

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(
    msg: Message,
    session: AsyncSession,
    user_service: UsersService,
) -> None:
    # data = UserSchema(
    #     chat_id=msg.chat.id,
    #     user_id=msg.from_user.id,
    #     username=msg.from_user.username,
    #     first_name=msg.from_user.first_name,
    #     last_name=msg.from_user.last_name,
    #     location=msg.location,
    #     contact=msg.contact
    # )
    # await user_service.create_user(session=session, data=data)
    paid_users = await user_service.get_paid_users(session=session)
    chat_ids = [paid_user.chat_id for paid_user in paid_users]

    if msg.chat.id in chat_ids:
        await msg.answer(
            text="Вы получаете оплаченный контент", parse_mode="HTML", reply_markup=start_reply_kb
        )
    else:
        await msg.answer(
            text="Вы должны оплатить!!! " "/buy", parse_mode="HTML", reply_markup=start_reply_kb
        )
