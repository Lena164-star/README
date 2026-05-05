from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from ..schemas import AnalyzeRequest, AnalyzeResponse
from ..ml_service import classifier
from ..models import RequestHistory
from ..db import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze(request: AnalyzeRequest, db: AsyncSession = Depends(get_db)):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(text) > 500:   # дополнительное ограничение (по желанию)
        raise HTTPException(status_code=400, detail="Text too long (max 500 characters)")

    try:
        label, score = classifier.predict(text)
    except Exception as e:
        logger.error(f"Model prediction error: {e}")
        raise HTTPException(status_code=500, detail="Model processing error")

    # Сохраняем в БД
    history_entry = RequestHistory(
        input_text=text,
        result_text=label,
        model_name=classifier.model_name
    )
    db.add(history_entry)
    await db.commit()

    logger.info(f"Analyzed text: label={label}, score={score}")
    return AnalyzeResponse(label=label, score=score)
