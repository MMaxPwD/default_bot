from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database.base import Base
from models.base import AuditMixin

if TYPE_CHECKING:
    from models.users import Users


class Payments(Base, AuditMixin):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(autoincrement=True, unique=True, primary_key=True)
    payment_id: Mapped[str] = mapped_column(nullable=False)
    chat_id: Mapped[int] = mapped_column(ForeignKey("users.chat_id"), nullable=False)
    status: Mapped[str]
    amount: Mapped[float] = mapped_column(default=0.0, nullable=False)

    user: Mapped["Users"] = relationship("Users", back_populates="payments")
