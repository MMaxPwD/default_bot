from typing import Any

from pydantic import BaseModel


class PaymentResponseSchema(BaseModel):
    conformation_url: str
    payment_status: str
    payment_id: str
    amount: float
    metadata: dict[str, Any]


class PaymentSchema(BaseModel):
    payment_id: str
    chat_id: int
    status: str
    amount: float


class PaymentUpdateSchema(BaseModel):
    payment_id: str | None = None
    chat_id: int | None = None
    status: str | None = None
    amount: float | None = None
