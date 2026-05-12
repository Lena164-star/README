import json
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import AnalyzeRequest, AnalyzeResponse
from ..database import get_db
from ..models import RequestHistory
from ..ml_service import spam_detector

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/analyze", response_model=AnalyzeResponse)
async def analyze_text(request: AnalyzeRequest, db: Session = Depends(get_db)):
    """Анализирует текст на спам и сохраняет результат в БД."""
    input_text = request.text.strip()
    logger.info(f"Received analysis request for text (first 50 chars): '{input_text[:50]}...'")
    
    if not input_text:
        raise HTTPException(status_code=400, detail="Input text cannot be empty")

    try:
        # Получаем предсказание от модели
        prediction = spam_detector.predict(input_text)
        # Преобразуем результат в JSON-строку для хранения
        result_text = json.dumps(prediction)
    except RuntimeError as e:
        logger.error(f"Model prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected prediction error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred during text analysis.")

    try:
        # Сохраняем запрос в БД
        db_history = RequestHistory(
            input_text=input_text,
            result_text=result_text,
            model_name=spam_detector.model_name
        )
        db.add(db_history)
        db.commit()
        db.refresh(db_history)
        logger.info(f"Request saved to database with id: {db_history.id}")
    except Exception as e:
        logger.error(f"Failed to save request to database: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to save request history.")

    return AnalyzeResponse(**prediction)
