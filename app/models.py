from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database import Base


class RequestHistory(Base):
    __tablename__ = "requests_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    input_text = Column(Text, nullable=False, comment="Original input text")
    result_text = Column(Text, nullable=False, comment="JSON: model result and score")
    model_name = Column(String(255), nullable=False, comment="Hugging Face model name")
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        comment="Timestamp of request"
    )

    def __repr__(self):
        return f"<RequestHistory(id={self.id}, model='{self.model_name}', created_at='{self.created_at}')>"
