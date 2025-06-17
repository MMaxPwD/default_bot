from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from uuid import uuid4

from sqlalchemy import NullPool
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.settings import settings


class DatabaseHelper:
    def __init__(self, db_uri: str, echo: bool) -> None:
        self.engine = create_async_engine(
            db_uri,
            echo=echo,
            poolclass=NullPool,
            connect_args={
                "server_settings": {"jit": "off"},
                "prepared_statement_name_func": lambda: f"__asyncpg_{uuid4()}__",
            },
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
            autoflush=False,
            autocommit=False,
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Асинхронный контекстный менеджер сессии с автоматическим commit/rollback для Aiogram"""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError:
                await session.rollback()
                raise  # Прокидываем исключение дальше
            finally:
                await session.close()

    async def session_dependency(self) -> AsyncGenerator[AsyncSession, None]:
        """Асинхронная фабрика сессии с автоматическим commit/rollback для Fastapi"""
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except SQLAlchemyError as e:
                await session.rollback()
                raise e  # Прокидываем исключение дальше


db_helper = DatabaseHelper(
    db_uri=settings.db_uri,
    echo=settings.DEBUG,
)
