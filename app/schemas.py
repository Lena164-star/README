from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Входные данные для /analyze
class AnalyzeRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Текст для проверки на спам")

# Выходные данные для /analyze
class AnalyzeResponse(BaseModel):
    result: str
    score: float

# Представление записи в истории для /history
class HistoryItem(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True # Позволяет создавать схему из ORM-модели
