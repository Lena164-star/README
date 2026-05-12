import json
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import AnalyzeRequest, AnalyzeResponse
from app.database import get_db
from app.models import RequestHistory
from app.ml_service import spam_detector

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("", response_model=AnalyzeResponse)
async def analyze_text(
    request: AnalyzeRequest,
    db: Session = Depends(get_db)
):
    """
    Анализирует текст и определяет, является ли он спамом.
    Результат сохраняется в историю запросов.
    """
    text = request.text.strip()

    # 1. Валидация входных данных
    if not text:
        logger.warning("Empty text received")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Input text cannot be empty"
        )

    logger.info(f"📝 Analyzing text: '{text[:100]}{'...' if len(text) > 100 else ''}'")

    # 2. Проверка готовности ML-модели
    if spam_detector is None:
        logger.error("ML model is not loaded")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ML model is not available. Please try again later."
        )

    # 3. Предсказание
    try:
        prediction = spam_detector.predict(text)
        result_json = json.dumps(prediction)
        logger.info(f"✅ Prediction: {prediction}")
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze text. Please try again."
        )

    # 4. Сохранение в БД
    try:
        db_record = RequestHistory(
            input_text=text,
            result_text=result_json,
            model_name=spam_detector.model_name
        )
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        logger.info(f"💾 Saved to history with ID: {db_record.id}")
    except Exception as e:
        logger.error(f"Failed to save to database: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Result was generated but could not be saved to history."
        )

    return AnalyzeResponse(**prediction)
