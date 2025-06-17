from fastapi import APIRouter

from api.yookassa import yookassa_router


api_router = APIRouter()
api_router.include_router(yookassa_router)
