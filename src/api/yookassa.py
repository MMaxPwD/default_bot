from fastapi import APIRouter, Request, Response

from core.logging.logging import logger
from dependencies.di_annotated import PaymentServiceDep, AsyncSessionDep

yookassa_router = APIRouter()


@yookassa_router.post("/webhook/yookassa/")
async def handle_webhook(
    request: Request, payment_service: PaymentServiceDep, session: AsyncSessionDep
) -> Response:
    try:
        data = await request.json()
        logger.info(f"✅ Yookassa Webhook получен: {data}")
        proceed_webhook = await payment_service.process_webhook(data=data, session=session)
        if proceed_webhook:
            return Response(status_code=200)
    except Exception as e:
        logger.error(f"❌ Ошибка Yookassa Webhook : {e}")
        return Response(status_code=400)
