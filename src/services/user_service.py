from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from models import Users
from repositories.users_repo import UsersRepository
from schemas.users import UserSchema, UserUpdateSchema


class UsersService:
    def __init__(
        self,
        repository: UsersRepository,
    ):
        self._repository = repository

    async def create_user(self, session: AsyncSession, data: UserSchema) -> Users:
        return await self._repository.create_user(session=session, data=data.model_dump())

    async def update_user(self, session: AsyncSession, data: dict[str, Any], chat_id: int) -> Users:
        return await self._repository.update_user(session=session, data=data, chat_id=chat_id)

    async def get_paid_users(self, session: AsyncSession) -> list[Users]:
        user_filter = UserUpdateSchema(
            is_paid=True,
        )
        return await self._repository.read_users_by_filter(session=session, user_filter=user_filter)
