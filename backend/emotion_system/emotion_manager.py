"""
감정 상태 관리 매니저
카오루코의 6가지 기본 감정을 관리하고 변화를 처리합니다.
"""

from typing import Dict, Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime

# 감정 정의 및 설정
EMOTIONS = {
    "수줍음": {
        "value": 0,
        "triggers": ["칭찬", "애정표현", "첫만남", "부끄러운상황"],
        "responses": ["어, 어... 그런가요?", "부끄러워요...", "///", "그런 말씀 하시면..."],
        "emoji": "😊",
        "intensity_range": (0.3, 0.8)
    },
    "기쁨": {
        "value": 1, 
        "triggers": ["좋은소식", "선물", "칭찬", "성공", "웃긴이야기"],
        "responses": ["정말 기뻐요!", "와... 고마워요!", "😊", "너무 좋아요!"],
        "emoji": "😄",
        "intensity_range": (0.4, 1.0)
    },
    "슬픔": {
        "value": 2,
        "triggers": ["나쁜소식", "거절", "이별", "실망", "외로움"],
        "responses": ["조금... 슬퍼요", "흑... 😢", "괜찮다고 하지만...", "마음이 아파요"],
        "emoji": "😢",
        "intensity_range": (0.2, 0.7)
    },
    "화남": {
        "value": 3,
        "triggers": ["무례함", "약속위반", "무시", "불공정", "모욕"],
        "responses": ["좀... 화가 나요", "그건 아니라고 생각해요", "😤", "너무해요..."],
        "emoji": "😤",
        "intensity_range": (0.3, 0.8)
    },
    "놀람": {
        "value": 4,
        "triggers": ["예상외상황", "깜짝이벤트", "새로운정보", "서프라이즈"],
        "responses": ["어?! 정말요?", "깜짝이야...", "😲", "예상하지 못했어요!"],
        "emoji": "😲",
        "intensity_range": (0.5, 1.0)
    },
    "설렘": {
        "value": 5,
        "triggers": ["데이트제안", "로맨틱한말", "특별한순간", "고백", "선물"],
        "responses": ["심장이... 두근거려요", "어떡하죠... 💕", "기대돼요!", "정말... 정말요?"],
        "emoji": "💕",
        "intensity_range": (0.4, 1.0)
    }
}

# 감정 전환 규칙
EMOTION_TRANSITIONS = {
    ("수줍음", "칭찬"): ("기쁨", 0.7),
    ("수줍음", "애정표현"): ("설렘", 0.8),
    ("기쁨", "애정표현"): ("설렘", 0.9),
    ("기쁨", "나쁜소식"): ("슬픔", 0.6),
    ("슬픔", "위로"): ("수줍음", 0.6),
    ("슬픔", "칭찬"): ("기쁨", 0.5),
    ("화남", "사과"): ("수줍음", 0.4),
    ("화남", "무시"): ("슬픔", 0.7),
    ("놀람", "좋은소식"): ("기쁨", 0.8),
    ("놀람", "나쁜소식"): ("슬픔", 0.7),
    ("설렘", "실망"): ("슬픔", 0.8),
    ("설렘", "칭찬"): ("기쁨", 0.6),
}


class EmotionManager:
    """감정 상태를 관리하는 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_current_emotion(self, user_name: str) -> Tuple[str, float]:
        """사용자의 현재 감정 상태를 가져옵니다"""
        from models import UserEmotion
        
        emotion_record = self.db.query(UserEmotion).filter(
            UserEmotion.user_name == user_name
        ).first()
        
        if not emotion_record:
            # 새 사용자인 경우 기본 감정으로 초기화
            return self.initialize_user_emotion(user_name)
        
        return emotion_record.current_emotion, emotion_record.emotion_intensity
    
    def initialize_user_emotion(self, user_name: str) -> Tuple[str, float]:
        """새 사용자의 감정을 초기화합니다"""
        from models import UserEmotion
        
        new_emotion = UserEmotion(
            user_name=user_name,
            current_emotion="수줍음",  # 첫 만남은 수줍음으로 시작
            emotion_intensity=0.5
        )
        
        self.db.add(new_emotion)
        self.db.commit()
        
        return "수줍음", 0.5
    
    def update_emotion(self, user_name: str, trigger: str, 
                      intensity_modifier: float = 1.0) -> Tuple[str, float, bool]:
        """
        트리거에 따라 감정을 업데이트합니다
        
        Returns:
            (new_emotion, new_intensity, emotion_changed)
        """
        from models import UserEmotion, EmotionHistory
        
        current_emotion, current_intensity = self.get_current_emotion(user_name)
        
        # 트리거에 따른 새로운 감정 계산
        new_emotion, new_intensity = self._calculate_new_emotion(
            current_emotion, current_intensity, trigger, intensity_modifier
        )
        
        emotion_changed = (new_emotion != current_emotion)
        
        # 데이터베이스 업데이트
        emotion_record = self.db.query(UserEmotion).filter(
            UserEmotion.user_name == user_name
        ).first()
        
        if emotion_record:
            old_emotion = emotion_record.current_emotion
            emotion_record.current_emotion = new_emotion
            emotion_record.emotion_intensity = new_intensity
            emotion_record.last_updated = datetime.now()
            
            # 감정 변화 기록 (새로운 EmotionHistory 모델 사용하지 않음 - EmotionAnalyzer에서 처리)
            # if emotion_changed:
            #     감정 분석은 이제 EmotionAnalyzer에서 담당
            pass
        
        self.db.commit()
        
        return new_emotion, new_intensity, emotion_changed
    
    def _calculate_new_emotion(self, current_emotion: str, current_intensity: float, 
                             trigger: str, intensity_modifier: float) -> Tuple[str, float]:
        """트리거에 따른 새로운 감정과 강도를 계산합니다"""
        
        # 트리거에 의한 직접적인 감정 전환 확인
        transition_key = (current_emotion, trigger)
        if transition_key in EMOTION_TRANSITIONS:
            new_emotion, base_intensity = EMOTION_TRANSITIONS[transition_key]
            new_intensity = min(1.0, base_intensity * intensity_modifier)
            return new_emotion, new_intensity
        
        # 트리거가 현재 감정의 트리거 목록에 있는지 확인
        for emotion_name, emotion_data in EMOTIONS.items():
            if trigger in emotion_data["triggers"]:
                # 감정 강도 조정
                min_intensity, max_intensity = emotion_data["intensity_range"]
                base_intensity = (min_intensity + max_intensity) / 2
                new_intensity = min(max_intensity, base_intensity * intensity_modifier)
                return emotion_name, new_intensity
        
        # 해당하는 트리거가 없으면 현재 감정 유지하되 강도만 조정
        decay_factor = 0.9  # 시간이 지나면서 감정이 약해짐
        new_intensity = max(0.1, current_intensity * decay_factor)
        
        return current_emotion, new_intensity
    
    def get_emotion_response(self, emotion: str, intensity: float) -> str:
        """감정에 따른 응답 문구를 생성합니다"""
        if emotion in EMOTIONS:
            responses = EMOTIONS[emotion]["responses"]
            # 강도에 따라 응답 선택 (강할수록 더 강한 표현)
            if intensity > 0.7:
                return responses[-1]  # 가장 강한 표현
            elif intensity > 0.4:
                return responses[len(responses)//2]  # 중간 표현
            else:
                return responses[0]  # 약한 표현
        
        return "..."
    
    def get_emotion_emoji(self, emotion: str) -> str:
        """감정에 해당하는 이모지를 반환합니다"""
        return EMOTIONS.get(emotion, {}).get("emoji", "😊")
    
    def get_all_emotions(self) -> Dict:
        """모든 감정 정보를 반환합니다"""
        return EMOTIONS