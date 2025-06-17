from typing import Any
from collections.abc import Callable, Awaitable

from aiogram.dispatcher.middlewares.base import BaseMiddleware

from core.database.db_helper import db_helper
from dependencies.di_annotated import get_user_service, get_payment_service


class DependencyMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        # Внедрение зависимостей сессий
        async with db_helper.session() as session:
            # Определение зависимостей
            data["session"] = session
            data["user_service"] = get_user_service()
            data["payment_service"] = get_payment_service()
            return await handler(event, data)
