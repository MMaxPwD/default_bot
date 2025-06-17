from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

from core.logging.logging import logger
from services.payments import PaymentService

payment_router = Router()


@payment_router.message(Command("buy"))
async def buy_handler(
    msg: Message,
    payment_service: PaymentService,
    session: AsyncSession,
) -> None:
    validated_payment = await payment_service.create_payment(
        amount="100", chat_id=msg.chat.id, session=session
    )
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Оплатить", url=validated_payment.conformation_url))
    builder.add(
        InlineKeyboardButton(
            text="Проверить оплату", callback_data=f"check_{validated_payment.payment_id}"
        )
    )

    await msg.answer("Счет сформирован", reply_markup=builder.as_markup())


@payment_router.callback_query(lambda c: "check" in c.data)
async def check_handler(
    callback: CallbackQuery,
    payment_service: PaymentService,
) -> None:
    result = await payment_service.get_payment(callback.data.split("_")[-1])

    logger.info(callback.data.split("_")[-1])
    if not result:
        await callback.message.answer("Оплата еще не прошла или возникла ошибка")
    else:
        await callback.message.answer("Оплата прошла успешно")
