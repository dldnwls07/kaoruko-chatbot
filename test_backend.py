"""
백엔드 API 테스트 스크립트
카오루코 챗봇의 응답을 직접 테스트합니다.
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

import google.generativeai as genai
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
import crud
import models

# 환경 변수 로드
load_dotenv(os.path.join('backend', '.env'))

# Gemini API 설정
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
else:
    print("❌ API 키가 설정되지 않았습니다!")
    exit(1)

# 데이터베이스 설정
DATABASE_URL = "sqlite:///./backend/chat_history.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 카오루코 페르소나
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

이 설정에 맞춰서 나와 대화해 줘. 너는 인공지능이라는 사실을 절대 드러내면 안 돼.
자연스럽고 수줍은 고등학생처럼 대화해야 해.
"""

def test_chat(user_message):
    """카오루코와 채팅 테스트"""
    print(f"\n👤 사용자: {user_message}")
    
    # DB 세션 생성
    db = SessionLocal()
    
    try:
        # 과거 대화 기록 조회
        chat_history = crud.get_chat_history(db, skip=0, limit=5)
        
        # 대화 컨텍스트 구성
        conversation_context = ""
        if chat_history:
            conversation_context = "\n\n최근 우리의 대화 내용:\n"
            for chat in reversed(chat_history):
                conversation_context += f"사용자: {chat.user_message}\n카오루코: {chat.bot_reply}\n"
        
        # 전체 프롬프트 구성
        full_prompt = f"{KAORUKO_PERSONA}\n{conversation_context}\n\n사용자의 새 메시지: {user_message}\n\n카오루코로서 답변해줘:"
        
        # Gemini API 호출
        response = model.generate_content(full_prompt)
        reply = response.text
        
        print(f"🌸 카오루코: {reply}")
        
        # 대화 내용 DB에 저장
        crud.create_chat_history(db=db, user_message=user_message, bot_reply=reply)
        print("✅ 대화 내용이 데이터베이스에 저장되었습니다.")
        
        return reply
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    print("🌸 카오루코 챗봇 테스트 시작!")
    print("=" * 50)
    
    # 테스트 대화들
    test_messages = [
        "안녕하세요 카오루코! 처음 뵙겠습니다",
        "오늘 학교는 어떠셨어요?",
        "어떤 케이크를 좋아하시나요?",
        "공부하시느라 힘드시죠?"
    ]
    
    for message in test_messages:
        test_chat(message)
        print("-" * 30)
    
    print("\n🎉 테스트 완료!")