import uuid

from yookassa import Payment
from yookassa.configuration import Configuration

from core.settings import settings
from schemas.payment import PaymentResponseSchema

# Передаем конфигурацию сразу же при импорте модуля
Configuration.configure(
    account_id=settings.SHOP_ID,
    secret_key=settings.SECRET_KEY,
)


class PaymentYookassaClient:
    def __init__(
        self,
        payment: Payment,
    ):
        self.payment = payment

    async def create_payment(self, amount: float, chat_id: int) -> PaymentResponseSchema:
        idempotence_key = str(uuid.uuid4())
        payment = self.payment.create(
            {
                "amount": {"value": amount, "currency": "RUB"},
                "payment_method_data": {"type": "bank_card"},
                "confirmation": {"type": "redirect", "return_url": f"{settings.BOT_URL}"},
                "notification_url": settings.NOTIFICATION_URL,
                "capture": True,
                "metadata": {"chat_id": chat_id},
                "description": "Оплата за услуги",
            },
            idempotence_key,
        )

        validated_payment = PaymentResponseSchema(
            conformation_url=payment.confirmation.confirmation_url,
            payment_status=payment.status,
            payment_id=payment.id,
            amount=payment.amount.value,
            metadata=payment.metadata,
        )
        return validated_payment

    async def get_payment(self, payment_id: str) -> str | bool:
        payment = self.payment.find_one(payment_id)
        if payment.status == "succeeded":
            return payment.metadata
        return False
