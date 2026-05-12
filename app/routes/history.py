import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas import HistoryItem
from app.database import get_db
from app.models import RequestHistory

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/history", tags=["History"])


@router.get("", response_model=List[HistoryItem])
async def get_recent_history(
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """
    Возвращает последние N запросов из истории (по умолчанию 20).
    """
    logger.info(f"📋 Fetching last {limit} history records")

    try:
        records = (
            db.query(RequestHistory)
            .order_by(RequestHistory.created_at.desc())
            .limit(limit)
            .all()
        )
        logger.info(f"✅ Found {len(records)} records")
        return records
    except Exception as e:
        logger.error(f"Failed to fetch history: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not retrieve history from database."
        )


@router.get("/{history_id}", response_model=HistoryItem)
async def get_history_by_id(
    history_id: int,
    db: Session = Depends(get_db)
):
    """
    Возвращает конкретную запись из истории по ID.
    """
    logger.info(f" Looking for history record ID: {history_id}")

    try:
        record = (
            db.query(RequestHistory)
            .filter(RequestHistory.id == history_id)
            .first()
        )
    except Exception as e:
        logger.error(f"Database query error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error querying database."
        )

    if record is None:
        logger.warning(f"Record ID {history_id} not found")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"History record with ID {history_id} not found."
        )

    logger.info(f"✅ Found record: ID={record.id}")
    return record
