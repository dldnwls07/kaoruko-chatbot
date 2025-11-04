# 🌸 카오루코 감정 시스템 업그레이드 계획서

## 📋 프로젝트 개요

### 🎯 목표
기존 카오루코 챗봇에 **감정 상태 시스템**과 **호감도 시스템**을 추가하여 더욱 생동감 있고 개인화된 대화 경험을 제공합니다.

### 🌟 핵심 기능
1. **감정 상태 시스템**: 카오루코의 현재 기분이 대화에 반영
2. **호감도 시스템**: 사용자와의 관계가 시간에 따라 발전
3. **동적 페르소나**: 감정과 호감도에 따른 말투 및 반응 변화

## 🎭 감정 시스템 설계

### 📊 감정 상태 정의
```python
EMOTIONS = {
    "수줍음": {
        "value": 0,
        "triggers": ["칭찬", "애정표현", "첫만남"],
        "responses": ["어, 어... 그런가요?", "부끄러워요...", "///"]
    },
    "기쁨": {
        "value": 1, 
        "triggers": ["좋은소식", "선물", "칭찬"],
        "responses": ["정말 기뻐요!", "와... 고마워요!", "😊"]
    },
    "슬픔": {
        "value": 2,
        "triggers": ["나쁜소식", "거절", "이별"],
        "responses": ["조금... 슬퍼요", "흑... 😢", "괜찮다고 하지만..."]
    },
    "화남": {
        "value": 3,
        "triggers": ["무례함", "약속위반", "무시"],
        "responses": ["좀... 화가 나요", "그건 아니라고 생각해요", "😤"]
    },
    "놀람": {
        "value": 4,
        "triggers": ["예상외상황", "깜짝이벤트", "새로운정보"],
        "responses": ["어?! 정말요?", "깜짝이야...", "😲"]
    },
    "설렘": {
        "value": 5,
        "triggers": ["데이트제안", "로맨틱한말", "특별한순간"],
        "responses": ["심장이... 두근거려요", "어떡하죠... 💕", "기대돼요!"]
    }
}
```

### 🔄 감정 변화 로직
```python
def update_emotion(current_emotion, trigger, intensity=1):
    # 트리거에 따른 감정 변화 규칙
    emotion_transitions = {
        ("수줍음", "칭찬"): ("기쁨", 0.7),
        ("기쁨", "애정표현"): ("설렘", 0.8),
        ("슬픔", "위로"): ("수줍음", 0.6),
        # ... 더 많은 전환 규칙
    }
```

## 💕 호감도 시스템 설계

### 📈 호감도 단계
```python
AFFECTION_LEVELS = {
    0-20: {
        "level": "낯선사람",
        "description": "조심스럽고 격식있는 대화",
        "speech_pattern": "존댓말, 거리감 있음",
        "unlock_features": []
    },
    21-40: {
        "level": "지인", 
        "description": "조금씩 마음을 열기 시작",
        "speech_pattern": "여전히 존댓말이지만 친근함 증가",
        "unlock_features": ["개인적인 이야기 공유"]
    },
    41-60: {
        "level": "친구",
        "description": "편안하고 자연스러운 대화",
        "speech_pattern": "가끔 반말, 농담도 함",
        "unlock_features": ["고민상담", "일상 이야기"]
    },
    61-80: {
        "level": "절친",
        "description": "깊은 신뢰와 애정",
        "speech_pattern": "자연스러운 반말, 애교도 부림",
        "unlock_features": ["비밀 이야기", "특별한 호칭"]
    },
    81-100: {
        "level": "특별한사람", 
        "description": "최고 단계의 친밀감",
        "speech_pattern": "완전히 편안함, 때로는 부끄러워함",
        "unlock_features": ["연인 모드", "특별 이벤트"]
    }
}
```

### 🎯 호감도 증가 요소
```python
AFFECTION_TRIGGERS = {
    "daily_chat": +1,           # 매일 대화
    "long_conversation": +2,     # 긴 대화 (10분 이상)
    "compliment": +3,           # 칭찬
    "remember_details": +5,      # 카오루코 정보 기억
    "gift_mention": +7,         # 선물 언급
    "romantic_gesture": +10,     # 로맨틱한 행동
    
    # 감소 요소
    "rude_behavior": -5,        # 무례한 행동
    "ignore_long_time": -3,     # 오랫동안 무시
    "inappropriate_content": -10 # 부적절한 내용
}
```

## 🏗️ 기술 구현 계획

### 📁 새로운 파일 구조
```
backend/
├── emotion_system/
│   ├── __init__.py
│   ├── emotion_manager.py      # 감정 상태 관리
│   ├── affection_manager.py    # 호감도 관리  
│   ├── response_generator.py   # 감정 기반 응답 생성
│   └── triggers.py            # 감정/호감도 트리거 감지
├── models.py                  # 기존 + 새로운 모델 추가
├── database.py                # 감정/호감도 테이블 추가
└── main.py                    # 감정 시스템 통합
```

### 🗄️ 데이터베이스 스키마 확장
```sql
-- 사용자 감정 상태 테이블
CREATE TABLE user_emotions (
    id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    current_emotion TEXT DEFAULT 'neutral',
    emotion_intensity FLOAT DEFAULT 0.5,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 호감도 테이블
CREATE TABLE user_affection (
    id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL UNIQUE,
    affection_level INTEGER DEFAULT 0,
    total_conversations INTEGER DEFAULT 0,
    first_met_date DATE DEFAULT CURRENT_DATE,
    last_interaction TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 감정 히스토리 테이블  
CREATE TABLE emotion_history (
    id INTEGER PRIMARY KEY,
    user_name TEXT NOT NULL,
    previous_emotion TEXT,
    new_emotion TEXT,
    trigger_type TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎨 프론트엔드 UI 개선

### 📊 감정 상태 표시
```jsx
// 카오루코의 현재 감정을 시각적으로 표시
const EmotionIndicator = ({ emotion, intensity }) => {
    const emotionEmojis = {
        "수줍음": "😊",
        "기쁨": "😄", 
        "슬픔": "😢",
        "화남": "😤",
        "놀람": "😲",
        "설렘": "💕"
    };
    
    return (
        <div className="emotion-indicator">
            <span className="emotion-emoji">{emotionEmojis[emotion]}</span>
            <div className="emotion-bar">
                <div 
                    className="emotion-fill"
                    style={{width: `${intensity * 100}%`}}
                />
            </div>
        </div>
    );
};
```

### 💕 호감도 프로그레스바
```jsx
const AffectionMeter = ({ level, progress }) => {
    return (
        <div className="affection-meter">
            <div className="affection-label">
                관계: {AFFECTION_LEVELS[level].level}
            </div>
            <div className="progress-bar">
                <div 
                    className="progress-fill"
                    style={{width: `${progress}%`}}
                />
            </div>
            <div className="hearts">
                {Array.from({length: 5}, (_, i) => (
                    <span key={i} className={i < level/20 ? 'filled' : 'empty'}>
                        💗
                    </span>
                ))}
            </div>
        </div>
    );
};
```

## 📝 구현 단계별 계획

### 🔷 1단계: 백엔드 기초 구조 (1-2일)
- [ ] 감정/호감도 관련 데이터베이스 테이블 생성
- [ ] 기본 감정 매니저 클래스 구현
- [ ] 호감도 매니저 클래스 구현
- [ ] API 엔드포인트 확장

### 🔷 2단계: 감정 시스템 로직 (2-3일)  
- [ ] 감정 트리거 감지 알고리즘
- [ ] 감정 전환 규칙 구현
- [ ] 감정 기반 응답 생성기
- [ ] 기존 Gemini 프롬프트에 감정 상태 통합

### 🔷 3단계: 호감도 시스템 (2-3일)
- [ ] 호감도 계산 로직
- [ ] 단계별 언락 기능
- [ ] 관계 발전 이벤트 시스템
- [ ] 장기 기억 시스템 통합

### 🔷 4단계: 프론트엔드 UI (2-3일)
- [ ] 감정 상태 시각화 컴포넌트
- [ ] 호감도 미터 컴포넌트  
- [ ] 관계 진행 상황 표시
- [ ] 특별 이벤트 알림 시스템

### 🔷 5단계: 통합 테스트 및 최적화 (1-2일)
- [ ] 전체 시스템 통합 테스트
- [ ] 성능 최적화
- [ ] 버그 수정 및 밸런스 조정
- [ ] 문서 업데이트

## 🎯 예상 결과

### 📈 개선 효과
1. **몰입감 증가**: 카오루코가 살아있는 캐릭터처럼 느껴짐
2. **재사용성 향상**: 매번 다른 반응으로 지루함 방지  
3. **개인화**: 사용자별로 다른 관계 발전 경험
4. **장기 사용**: 호감도 시스템으로 지속적 사용 동기 부여

### 🎭 대화 예시 변화

#### 호감도 20 (낯선사람)
**사용자**: "오늘 날씨 좋네요!"  
**카오루코**: "네... 정말 좋은 날씨인 것 같아요. 산책하기 좋을 것 같네요." 😊

#### 호감도 60 (친구)  
**사용자**: "오늘 날씨 좋네요!"
**카오루코**: "정말요! 이런 날엔 같이 학교 뒷산에 올라가서 도시락 먹고 싶어져요~ 어때요?" 😄

#### 호감도 90 (특별한사람)
**사용자**: "오늘 날씨 좋네요!"  
**카오루코**: "후훗... 그러게요! 혹시... 저랑 같이 벚꽃 보러 갈까요? 아, 이상한 뜻은 아니고... 그냥... 💕" 😳

## ⚠️ 주의사항 및 고려사항

### 🔒 개인정보 보호
- 감정/호감도 데이터는 로컬에만 저장
- 사용자 동의 없이 외부 전송 금지
- 데이터 초기화 옵션 제공

### ⚖️ 밸런스 조정
- 호감도 상승이 너무 빠르지 않도록 조절
- 감정 변화가 자연스럽게 느껴지도록
- 극단적인 반응 방지

### 🎯 사용자 경험
- 시스템이 복잡하지 않고 직관적이어야 함
- 선택적 기능으로 on/off 가능
- 기존 사용자의 데이터 마이그레이션 고려

---

## 📅 개발 일정

- **총 예상 기간**: 8-12일
- **시작일**: 2025년 11월 4일
- **1차 완성 목표**: 2025년 11월 16일
- **최종 테스트**: 2025년 11월 18일

**🌸 카오루코가 더욱 생생하게 살아날 준비가 되었습니다!**