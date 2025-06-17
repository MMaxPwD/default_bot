from typing import Any
from core.logging.logging import logger
from sqlalchemy import update, select, literal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.users import Users
from schemas.users import UserUpdateSchema


class UsersRepository:
    _model: type[Users] = Users

    async def create_user(self, session: AsyncSession, data: dict[str, Any]) -> Users:
        try:
            record = self._model(**data)
            session.add(record)
            await session.flush()
            return record

        except SQLAlchemyError:
            logger.error("Пользователь уже существует")

    async def update_user(self, session: AsyncSession, data: dict[str, Any], chat_id: int) -> Users:
        try:
            query = (
                update(self._model)
                .values(**data)
                .where(self._model.chat_id == literal(chat_id))
                .returning(self._model)
            )
            user = await session.scalar(query)
            return user
        except SQLAlchemyError as e:
            logger.error(f"Ошибка обновления пользователя: {e}")
            raise

    async def read_users_by_filter(
        self, session: AsyncSession, user_filter: UserUpdateSchema
    ) -> list[Users]:
        try:
            query = select(self._model)
            if user_filter.is_paid:
                query = query.where(self._model.is_paid == literal(user_filter.is_paid))
            users = await session.scalars(query)
            return list(users)
        except SQLAlchemyError as e:
            logger.error(f"Ошибка получения пользователей: {e}")
            raise
