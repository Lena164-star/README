from pydantic import BaseModel, Field
from datetime import datetime


class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Text to classify as SPAM or NOT SPAM",
        examples=["Congratulations! You've won a free iPhone!"]
    )


class AnalyzeResponse(BaseModel):
    result: str = Field(..., description="SPAM or NOT SPAM")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")


class HistoryItem(BaseModel):
    id: int
    input_text: str
    result_text: str
    model_name: str
    created_at: datetime

    class Config:
        from_attributes = True


class HealthResponse(BaseModel):
    status: str = "ok"
