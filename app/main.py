from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging
from .db import engine, Base
from .routes import analyze, history
from .config import LOG_LEVEL

logging.basicConfig(level=LOG_LEVEL, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables ensured")
    yield
    # при завершении ничего не делаем

app = FastAPI(title="AI Spam Detector", lifespan=lifespan)
app.include_router(analyze.router, prefix="")
app.include_router(history.router, prefix="")

@app.get("/health")
async def health():
    return {"status": "ok"}
