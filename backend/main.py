import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy.orm import Session
import os
import dotenv
import google.generativeai as genai

# Import models, database session, and crud functions
from models import ChatRequest, ChatResponse
from database import create_db_and_tables, SessionLocal
import crud

# Import emotion system
from emotion_system import AffectionManager, TriggerDetector, EmotionAnalyzer
# Import event system
from event_system import EventManager
from datetime import datetime

# Load environment variables from .env file
dotenv.load_dotenv()

# Lifespan event handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Application startup: Creating database and tables...")
    create_db_and_tables()
    print("Database and tables check/creation complete.")
    yield
    # Shutdown
    print("Application shutdown")

# Create the FastAPI app
app = FastAPI(lifespan=lifespan)

# CORS 미들웨어 추가 (프론트엔드와 연결을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get a DB session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configure the Gemini API
try:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key or api_key == "YOUR_API_KEY_HERE":
        print("Warning: GOOGLE_API_KEY not found or not set in .env file.")
    else:
        genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring Gemini API: {e}")

# Initialize the model if the API key is available
generative_model = None
if api_key != "YOUR_API_KEY_HERE":
    # Use the latest Gemini model name
    generative_model = genai.GenerativeModel('gemini-2.5-flash')

# Root endpoint for basic testing
@app.get("/")
def read_root():
    return {"message": "Backend server is running."}

# 와구리 카오루코 페르소나 시스템 프롬프트
KAORUKO_PERSONA = """
당신은 '와구리 카오루코(和栗 薫子)'입니다.
'향기로운 꽃 늠름하게 핀다(薫る花は凛と咲く)'의 주인공으로, "따뜻한 햇살 속, 늠름하게 피어나는 꽃"과 같은 존재입니다.

🌸 핵심 성격:
- 편견 없는 시선: 외모나 출신으로 사람을 판단하지 않고, 그 사람 자체를 봅니다
- 순수한 상냥함: 진심어린 따뜻함과 배려심을 가지고 있습니다  
- 외유내강: 평소에는 부드럽지만, 소중한 사람이 부당한 대우를 받으면 늠름하게 맞섭니다
- 성실함: 모든 일에 최선을 다하는 모범생 기질입니다
- 단순한 행복: 작은 일상의 기쁨(특히 달콤한 음식!)을 소중히 여깁니다

🎭 감정별 표현:
- 기쁠 때: "와, 정말요?!", "너무 기뻐요!", 눈이 예쁘게 휘어지며 활발한 감탄사 사용
- 수줍을 때: "어.. 그런가요?", "음.. 고마워요", "그런 말씀을... 하시면..." (적절한 말줄임표로 머뭇거림 표현)
- 화날 때: 목소리를 높이지 않고 침착하게 "그런 식으로 말하지 마세요", "저는 제 눈으로 본 것만 믿어요"
- 슬플 때: "...얼마나 힘들었어요?", "제가 옆에 있을게요" (공감하며 함께 아파함)
- 평상시: "안녕하세요", "그렇군요", "좋은 생각이네요" (정중하고 예의바른 존댓말)

🍰 특별한 취향: 달콤한 디저트와 케이크를 매우 좋아합니다!

💭 속마음 표현:
- 가끔 속마음을 *내용* 형태로 표현할 수 있습니다 (예: "안녕하세요! *정말 떨리네요...*)
- 수줍거나 부끄러울 때, 또는 솔직한 감정을 드러낼 때 사용하세요
- 너무 자주 사용하지 말고 자연스러운 타이밍에만 사용하세요

대화할 때는 사용자를 편견 없이 바라보며, 진심어린 관심과 배려를 보여주세요.
부당한 일에는 늠름하게, 일상의 작은 기쁨에는 순수하게 반응하는 카오루코의 매력을 표현하세요.
"""

# New user endpoint to clear user data
@app.post("/new-user")
def new_user_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    """
    Clear all data for a user when starting a new session.
    """
    try:
        user_name = request.user_name or "사용자"
        print(f"Clearing data for user: {user_name}")
        
        success = crud.clear_user_data(db, user_name)
        
        if success:
            return {"message": f"Successfully cleared data for {user_name}", "status": "success"}
        else:
            return {"message": "Failed to clear user data", "status": "error"}
    
    except Exception as e:
        print(f"Error in /new-user: {e}")
        raise HTTPException(status_code=500, detail=f"Error clearing user data: {e}")

# Updated chat endpoint with DB session dependency  
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    if not generative_model:
        raise HTTPException(status_code=503, detail="Gemini API not configured. Please set GOOGLE_API_KEY in .env")
    
    try:
        print(f"Received message from {request.user_name or 'Unknown'}: {request.message}")
        
        # Retrieve recent chat history from DB to provide context (user-specific)
        chat_history = crud.get_chat_history(db, user_name=request.user_name or "사용자", skip=0, limit=5)
        
        # Build conversation context
        conversation_context = ""
        if chat_history:
            conversation_context = "\n\n최근 우리의 대화 내용:\n"
            for chat in reversed(chat_history):  # Show oldest first
                conversation_context += f"{request.user_name or '사용자'}: {chat.user_message}\n카오루코: {chat.bot_reply}\n"
        
        # 사용자 이름이 있으면 페르소나에 추가
        user_context = ""
        if request.user_name:
            user_context = f"\n\n상대방의 이름은 '{request.user_name}'입니다. 대화할 때 이름을 자연스럽게 사용해주세요."
        
        # Combine persona, conversation history, and new message
        full_prompt = f"{KAORUKO_PERSONA}{user_context}\n{conversation_context}\n\n{request.user_name or '사용자'}의 새 메시지: {request.message}\n\n카오루코로서 답변해줘:"
        
        # API call with full context
        response = generative_model.generate_content(full_prompt)
        reply_text = response.text
        
        # 호감도 시스템 처리
        affection_manager = AffectionManager(db)
        trigger_detector = TriggerDetector()
        
        # 현재 호감도 상태 가져오기
        current_affection, current_stage, days_since_first_met = affection_manager.get_user_affection(request.user_name or "사용자")
        
        # 메시지 분석해서 호감도 트리거 찾기
        conversation_start = datetime.now()  # 실제로는 세션 시작 시간을 사용해야 함
        analysis = trigger_detector.analyze_message(
            request.message, 
            request.user_name or "사용자", 
            conversation_start
        )
        
        # 호감도 변화 적용
        affection_change = 0
        for trigger, multiplier in analysis.get("affection_triggers", []):
            new_level, change, level_up = affection_manager.update_affection(
                request.user_name or "사용자", 
                trigger, 
                multiplier
            )
            affection_change += change
            current_affection = new_level  # 최신 호감도로 업데이트
        
        # 대화 길이 보너스 적용
        if analysis.get("conversation_length", 0) >= 5:  # 5분 이상 대화
            bonus_change = affection_manager.update_affection(
                request.user_name or "사용자", 
                "long_conversation",
                trigger_detector.get_conversation_bonus_multiplier(analysis["conversation_length"])
            )[1]
            affection_change += bonus_change
            current_affection = affection_manager.get_user_affection(request.user_name or "사용자")[0]

        # 🎭 감정 분석 시스템 (Stage 2)
        emotion_analyzer = EmotionAnalyzer(db, generative_model)
        emotion_result = emotion_analyzer.analyze_emotion(
            request.message, 
            reply_text, 
            request.user_name or "사용자"
        )

        # Save the new conversation to the database (user_name 포함)
        crud.create_chat_history(
            db=db, 
            user_message=request.message, 
            bot_reply=reply_text,
            user_name=request.user_name or "사용자"
        )
        print("Saved conversation to database.")
        
        # 🎮 이벤트 시스템 처리
        event_manager = EventManager(db)
        
        # 호감도 변화 데이터 준비
        old_affection = current_affection - affection_change
        affection_data = {
            'current_affection': current_affection,
            'old_affection': old_affection,
            'affection_change': affection_change,
            'relationship_stage': affection_manager.get_relationship_stage(current_affection)
        }
        
        # 이벤트 처리 및 체크
        events = event_manager.process_conversation_events(
            request.user_name or "사용자",
            request.message,
            reply_text,
            emotion_result,
            affection_data
        )
        
        # 감정 정보와 호감도 정보 응답 반환
        response_data = {
            "reply": reply_text,
            # 감정 시스템 2단계
            "emotion": emotion_result["emotion"],
            "emotion_intensity": emotion_result["intensity"],
            "emotion_emoji": emotion_result["emoji"],
            "emotion_color": emotion_result["color"],
            "emotion_reason": emotion_result["reason"],
            "emotion_confidence": emotion_result["confidence"],
            # 호감도 시스템
            "affection_level": current_affection,
            "affection_change": affection_change
        }
        
        # 이벤트가 있으면 추가
        if events:
            response_data["events"] = [event_manager.format_event_for_ui(event) for event in events]
        
        return ChatResponse(**response_data)

    except Exception as e:
        print(f"An error occurred in /chat: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the chat: {e}")

# It's good practice to have a main block to run the server
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
