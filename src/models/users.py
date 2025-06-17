from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from models.base import AuditMixin

if TYPE_CHECKING:
    from models.payments import Payments


class Users(Base, AuditMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    username: Mapped[str | None] = mapped_column(nullable=True)
    chat_id: Mapped[int] = mapped_column(unique=True)
    user_id: Mapped[int]
    first_name: Mapped[str | None] = mapped_column(nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    location: Mapped[str | None] = mapped_column(nullable=True)
    contact: Mapped[str | None] = mapped_column(nullable=True)
    is_paid: Mapped[bool | None] = mapped_column(default=False, nullable=True)

    payments: Mapped[list["Payments"]] = relationship("Payments", back_populates="user")

    def __repr__(self) -> str:
        return (
            f"\n"
            f'<"username": "{self.username}";'
            f' "name": "{self.first_name}";'
            f' "chat_id": "{self.chat_id}">'
        )

    def as_dict(self) -> dict[str, Any]:
        result = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)
            if isinstance(value, datetime):
                result[c.name] = value.isoformat()
                # Преобразует дату в строку 'YYYY-MM-DDTHH:MM:SS'
            else:
                result[c.name] = value
        return result
