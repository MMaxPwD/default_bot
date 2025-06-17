from typing import Any
from core.logging.logging import logger
from sqlalchemy import update, literal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models import Payments


class PaymentRepository:
    _model: type[Payments] = Payments

    async def create_payment(self, session: AsyncSession, data: dict[str, Any]) -> Payments:
        try:
            record = self._model(**data)
            session.add(record)
            await session.flush()
            return record

        except SQLAlchemyError as e:
            logger.error(f"Платеж не сохранен в БД {e}")
            raise

    async def update_payment(
        self, session: AsyncSession, payment_id: str, data: dict[str, Any]
    ) -> Payments:
        try:
            query = (
                update(self._model)
                .values(**data)
                .where(self._model.payment_id == literal(payment_id))
                .returning(self._model)
            )
            payment = await session.scalar(query)
            return payment
        except SQLAlchemyError as e:
            logger.error(f"Ошибка обновления платежа: {e}")
            raise
