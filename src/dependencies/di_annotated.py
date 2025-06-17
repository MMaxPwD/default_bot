from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from yookassa import Payment

from core.database.db_helper import db_helper
from repositories.payment_repo import PaymentRepository
from repositories.payment_yoocassa import PaymentYookassaClient
from repositories.users_repo import UsersRepository
from services.payments import PaymentService
from services.user_service import UsersService


@cache
def get_user_repository() -> UsersRepository:
    """Фабрика с кэшированием репозитория пользователей."""
    return UsersRepository()


@cache
def get_user_service() -> UsersService:
    """Фабрика с кэшированием сервиса пользователей."""
    return UsersService(repository=get_user_repository())


@cache
def get_payment_client() -> PaymentYookassaClient:
    """Фабрика с кэшированием клиента yookassa."""
    return PaymentYookassaClient(payment=Payment())


@cache
def get_payment_repository() -> PaymentRepository:
    """Фабрика с кэшированием репозитория платежей."""
    return PaymentRepository()


@cache
def get_payment_service() -> PaymentService:
    """Фабрика с кэшированием сервиса платежей."""
    return PaymentService(
        payment_repository=get_payment_repository(),
        payment_client=get_payment_client(),
        user_service=get_user_service(),
    )


# Для вебхуков на роутах FastAPI
PaymentServiceDep = Annotated[PaymentService, Depends(get_payment_service)]
AsyncSessionDep = Annotated[AsyncSession, Depends(db_helper.session_dependency)]
