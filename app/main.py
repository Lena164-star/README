import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.database import engine, Base
from app.routes import analyze, history

# ============ Настройка логирования ============
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


# ============ Жизненный цикл приложения ============
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Запускается при старте и завершении работы приложения."""
    logger.info("=" * 50)
    logger.info("🚀 Starting AI Spam Detector API...")
    logger.info("=" * 50)

    # Создание таблиц в БД при старте
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("✅ Database tables checked/created")
    except Exception as e:
        logger.error(f"❌ Failed to create tables: {e}")

    yield  # Здесь приложение работает

    logger.info("🛑 Shutting down AI Spam Detector API...")


# ============ Создание приложения ============
app = FastAPI(
    title="AI Spam Detector API",
    description="REST API для классификации текста как SPAM / NOT SPAM с использованием Hugging Face моделей",
    version="1.0.0",
    lifespan=lifespan,
)

# Подключаем роутеры
app.include_router(analyze.router)
app.include_router(history.router)


# ============ Middleware для логирования запросов ============
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования всех HTTP-запросов."""
    logger.info(f"➡️ {request.method} {request.url.path} from {request.client.host}")
    
    try:
        response = await call_next(request)
        logger.info(f"⬅️ {request.method} {request.url.path} - Status: {response.status_code}")
        return response
    except Exception as e:
        logger.error(f"❌ Unhandled error: {e}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )


# ============ Health Check ============
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Проверка работоспособности сервиса.
    
    Возвращает OK, если сервис запущен.
    """
    logger.info("💚 Health check requested")
    return {"status": "ok"}


# ============ Корневой эндпоинт ============
@app.get("/", tags=["Root"])
async def root():
    """Информация о сервисе."""
    return {
        "service": "AI Spam Detector API",
        "version": "1.0.0",
        "endpoints": {
            "POST /analyze": "Analyze text for spam",
            "GET /history": "Get last 20 requests",
            "GET /history/{id}": "Get specific request by ID",
            "GET /health": "Health check",
        }
    }


# ============ Точка входа ============
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
