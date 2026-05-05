from pydantic import BaseModel
from datetime import datetime

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    label: str       # "spam" / "ham"
    score: float

class HistoryItem(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True
