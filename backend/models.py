from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Date
from sqlalchemy.sql import func
from database import Base
from typing import List, Dict

# --- Pydantic Models for API validation ---

# Request model for the chat endpoint
class ChatRequest(BaseModel):
    message: str
    user_name: str = ""  # 사용자 이름 (선택적)

# Response model for the chat endpoint
class ChatResponse(BaseModel):
    reply: str
    # 감정 시스템 2단계
    emotion: str = "수줍음" 
    emotion_intensity: int = 5
    emotion_emoji: str = "😊"
    emotion_color: str = "#ffb3d9"
    emotion_reason: str = ""
    emotion_confidence: float = 0.8
    # 호감도 시스템
    affection_level: int = 0
    affection_change: int = 0
    # 이벤트 시스템
    events: List[Dict] = []


# --- 감정 시스템 API 모델들 ---

class EmotionStatus(BaseModel):
    """감정 상태 응답 모델"""
    current_emotion: str
    emotion_intensity: float
    affection_level: int
    relationship_stage: str


class AffectionUpdate(BaseModel):
    """호감도 업데이트 요청 모델"""
    user_name: str
    affection_change: int
    trigger_type: str = ""


# --- SQLAlchemy Model for Database ---

class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_message = Column(String, nullable=False)
    bot_reply = Column(String, nullable=False)
    user_name = Column(String, nullable=True)  # 사용자 이름 추가
    timestamp = Column(DateTime(timezone=True), server_default=func.now())


# --- 감정 시스템 모델들 ---

class UserEmotion(Base):
    """사용자별 현재 감정 상태"""
    __tablename__ = "user_emotions"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True, index=True)
    current_emotion = Column(String, default="수줍음")  # 기본 감정
    emotion_intensity = Column(Float, default=0.5)  # 감정 강도 (0.0-1.0)
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class UserAffection(Base):
    """사용자별 호감도 정보"""
    __tablename__ = "user_affection"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, unique=True, index=True)
    affection_level = Column(Integer, default=0)  # 호감도 (0-100)
    total_conversations = Column(Integer, default=0)  # 총 대화 횟수
    first_met_date = Column(Date, default=func.current_date())  # 첫 만남 날짜
    last_interaction = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class EmotionHistory(Base):
    """감정 분석 기록 (Stage 2)"""
    __tablename__ = "emotion_history"

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False, index=True)
    emotion = Column(String, nullable=False)  # 분석된 감정 (수줍음, 기쁨, 슬픔, 화남, 놀람, 설렘)
    intensity = Column(Integer, default=5)  # 감정 강도 (1-10)
    reason = Column(Text, nullable=True)  # 감정 분석 이유
    confidence = Column(Float, default=0.8)  # 분석 확신도 (0.0-1.0)
    trigger_type = Column(String, nullable=True)  # 감정 변화 원인  
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
