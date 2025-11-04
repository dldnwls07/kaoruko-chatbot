from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

# --- Pydantic Models for API validation ---

# Request model for the chat endpoint
class ChatRequest(BaseModel):
    message: str
    user_name: str = ""  # 사용자 이름 (선택적)

# Response model for the chat endpoint
class ChatResponse(BaseModel):
    reply: str


# --- SQLAlchemy Model for Database ---

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    bot_reply = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
