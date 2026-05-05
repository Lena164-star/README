from sqlalchemy import Column, Integer, String, Text, DateTime, func
from .db import Base

class RequestHistory(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(Text, nullable=False)
    result_text = Column(String, nullable=False)   # например, "spam" или "ham"
    model_name = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
