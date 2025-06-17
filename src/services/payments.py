from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from core.logging.logging import logger
from models import Payments
from repositories.payment_repo import PaymentRepository
from repositories.payment_yoocassa import PaymentYookassaClient
from schemas.enum import PaymentStatusEnum
from schemas.payment import PaymentResponseSchema, PaymentSchema, PaymentUpdateSchema
from schemas.users import UserUpdateSchema
from services.user_service import UsersService


class PaymentService:
    def __init__(
        self,
        payment_repository: PaymentRepository,
        payment_client: PaymentYookassaClient,
        user_service: UsersService,
    ):
        self._payment_repository = payment_repository
        self._payment_client = payment_client
        self._user_service = user_service

    async def create_payment(
        self, session: AsyncSession, amount: float, chat_id: int
    ) -> PaymentResponseSchema:
        # Создаем платеж в Yookassa
        payment = await self._payment_client.create_payment(amount=amount, chat_id=chat_id)
        if not payment:
            raise Exception("Платеж в Yookassa не создан")

        # Сохраняем платеж в БД
        updated_payment = PaymentSchema(
            payment_id=payment.payment_id,
            chat_id=chat_id,
            status=payment.payment_status,
            amount=payment.amount,
        )
        payment_record = await self._payment_repository.create_payment(
            session=session, data=updated_payment.model_dump()
        )
        if not payment_record:
            raise Exception("Платеж не сохранен в БД")

        return payment

    async def update_payment(
        self, session: AsyncSession, payment_id: str, data: dict[str, Any]
    ) -> Payments:
        updated_payment = PaymentUpdateSchema.model_validate(data)
        return await self._payment_repository.update_payment(
            session=session,
            payment_id=payment_id,
            data=updated_payment.model_dump(exclude_unset=True),
        )

    async def get_payment(self, payment_id: str) -> str | bool:
        """Получение статуса платежа"""
        return await self._payment_client.get_payment(payment_id)

    async def process_webhook(self, session: AsyncSession, data: dict[str, Any]) -> bool:
        """Обработка уведомлений yookassa"""
        # Валидируем данные
        payment_id = data["object"]["id"]
        payment_status = data["object"]["status"]
        validated_data = PaymentUpdateSchema(
            status=payment_status,
        )

        # Обновляем статус платежа из уведомления и получаем chat_id платежа.
        payment = await self.update_payment(
            payment_id=payment_id,
            data=validated_data.model_dump(exclude_unset=True),
            session=session,
        )
        if not payment:
            raise Exception("Платеж не обновлен")
        logger.info(f"Платеж {payment_id} обновлен")
        chat_id = payment.chat_id

        # Обновляем статус пользователя.
        if payment_status == PaymentStatusEnum.SUCCEEDED:
            updated_user = UserUpdateSchema(is_paid=True)
            await self._user_service.update_user(
                session=session, data=updated_user.model_dump(exclude_unset=True), chat_id=chat_id
            )
            logger.info(f"Доступ к платному контенту для пользователя {chat_id} предоставлен")
            return True
        raise Exception("Неизвестный статус платежа")
