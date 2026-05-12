import logging
from fastapi import FastAPI, Request
from .database import engine, Base
from .routes import analyze, history

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаем таблицы в БД (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Spam Detector", version="1.0.0")

# Подключаем роутеры эндпоинтов
app.include_router(analyze.router, tags=["Analysis"])
app.include_router(history.router, tags=["History"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Middleware для логирования входящих запросов."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    return response

@app.get("/health", tags=["Health Check"])
async def health_check():
    """Эндпоинт для проверки работоспособности сервиса."""
    logger.info("Health check requested.")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
