from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..models import RequestHistory
from ..schemas import HistoryItem
from ..db import get_db

router = APIRouter()

@router.get("/history", response_model=list[HistoryItem])
async def get_recent_history(db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(RequestHistory).order_by(RequestHistory.created_at.desc()).limit(20)
    )
    return result.scalars().all()

@router.get("/history/{id}", response_model=HistoryItem)
async def get_history_by_id(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(RequestHistory).where(RequestHistory.id == id))
    entry = result.scalar_one_or_none()
    if not entry:
        raise HTTPException(status_code=404, detail="History entry not found")
    return entry
