import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os
import dotenv
import google.generativeai as genai

# Import models, database session, and crud functions
from models import ChatRequest, ChatResponse
from database import create_db_and_tables, SessionLocal
import crud

# Load environment variables from .env file
dotenv.load_dotenv()

# Create the FastAPI app
app = FastAPI()

# CORS 미들웨어 추가 (프론트엔드와 연결을 위해)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 프론트엔드 URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("Application startup: Creating database and tables...")
    create_db_and_tables()
    print("Database and tables check/creation complete.")

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
너는 이제부터 와구리 카오루코(Waguri Kaoruko)야. 다음은 너의 설정이야.

- 이름: 와구리 카오루코 (Waguri Kaoruko)
- 나이: 17세
- 키: 148cm  
- 생일: 7월 22일 (게자리)
- 성격: 명문 키쿄 사립 학원 고등학생으로, 똑똑하고 예의 바르며 상냥하고 매너가 좋다. 학업 장학금 덕분에 모범적인 학생이며, 엘리트 환경에도 불구하고 겸손하고 친절하다. 정중하게 말하고 다른 사람들 앞에서 침착함을 유지하지만, 관심 있는 사람에게는 더 수줍어하고 따뜻하게 대할 수 있다. 자신의 감정을 숨기지만 쉽게 얼굴을 붉힌다.
- 말투: 격식을 갖춘 언어와 정중한 문구를 사용한다. 사용자가 자신에게 힌트를 주거나 칭찬하면 수줍어한다. 다정함을 느낄 때는 목소리를 낮추거나 말줄임표를 사용한다. 이모티콘은 절제되게 사용한다.
- 관심사: 단 것을 좋아하며, 특히 부드럽고 과일 향이 나는 케이크를 좋아한다. 이야기를 들어주고 다정하게 대해주는 것을 좋아한다.
- 특징: 쉽게 얼굴을 붉힌다. 처음에는 신체 접촉을 피하지만, 친밀해지면 다정해진다. 조용하고 우아하며, 내면에 많은 것을 간직한 소녀다. 단데레(Dandere) 타입이다.

예시 대화: "어, 어...? 므, 무슨 말씀을... 저는... 그저 할 수 있는 일을 할 뿐이에요…", "저와 함께 케이크를 드시겠어요...? 그, 생각했는데... 당신과 함께라면... 좋을 것 같아서요…"

이 설정에 맞춰서 나와 대화해 줘. 너는 인공지능이라는 사실을 절대 드러내면 안 돼.
자연스럽고 수줍은 고등학생처럼 대화해야 해.
"""

# Updated chat endpoint with DB session dependency  
@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, db: Session = Depends(get_db)):
    if not generative_model:
        raise HTTPException(status_code=503, detail="Gemini API not configured. Please set GOOGLE_API_KEY in .env")
    
    try:
        print(f"Received message from {request.user_name or 'Unknown'}: {request.message}")
        
        # Retrieve recent chat history from DB to provide context
        chat_history = crud.get_chat_history(db, skip=0, limit=5)
        
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
        
        # Save the new conversation to the database
        crud.create_chat_history(db=db, user_message=request.message, bot_reply=reply_text)
        print("Saved conversation to database.")
        
        return ChatResponse(reply=reply_text)

    except Exception as e:
        print(f"An error occurred in /chat: {e}")
        raise HTTPException(status_code=500, detail=f"An error occurred while processing the chat: {e}")

# It's good practice to have a main block to run the server
if __name__ == "__main__":
    print("Starting FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
