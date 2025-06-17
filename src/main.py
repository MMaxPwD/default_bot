import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routes import api_router
from core.lifespan.lifespan import lifespan
from core.settings import settings

app = FastAPI(lifespan=lifespan)
app.include_router(api_router)

# CORS для тестов через ngrok
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        access_log=False,
        reload=True,
    )
