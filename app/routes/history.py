import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..schemas import HistoryItem
from ..database import get_db
from ..models import RequestHistory

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/history", response_model=List[HistoryItem])
async def get_history(db: Session = Depends(get_db)):
    """Возвращает последние 20 запросов из истории."""
    logger.info("Fetching last 20 history items.")
    try:
        history = (
            db.query(RequestHistory)
            .order_by(RequestHistory.created_at.desc())
            .limit(20)
            .all()
        )
        return history
    except Exception as e:
        logger.error(f"Failed to fetch history: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history.")

@router.get("/history/{history_id}", response_model=HistoryItem)
async def get_history_item(history_id: int, db: Session = Depends(get_db)):
    """Возвращает конкретную запись из истории по ID."""
    logger.info(f"Fetching history item with id: {history_id}")
    try:
        history_item = db.query(RequestHistory).filter(RequestHistory.id == history_id).first()
        if history_item is None:
            raise HTTPException(status_code=404, detail=f"History item with id {history_id} not found.")
        return history_item
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to fetch history item {history_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history item.")
