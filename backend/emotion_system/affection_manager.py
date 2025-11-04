"""
호감도 시스템 관리 매니저
사용자와 카오루코의 관계 발전을 관리합니다.
"""

from typing import Dict, Tuple, Optional
from sqlalchemy.orm import Session
from datetime import datetime, date
import math

# 호감도 단계 정의
AFFECTION_LEVELS = {
    (-100, -1): {
        "level": "멀어진사람",
        "description": "거리를 두고 경계하는 상태",
        "speech_pattern": "짧고 단호한 표현",
        "unlock_features": [],
        "title": ""
    },
    (0, 20): {
        "level": "낯선사람",
        "description": "조심스럽고 격식있는 대화",
        "speech_pattern": "존댓말, 거리감 있음",
        "unlock_features": [],
        "title": "님"
    },
    (21, 40): {
        "level": "지인", 
        "description": "조금씩 마음을 열기 시작",
        "speech_pattern": "여전히 존댓말이지만 친근함 증가",
        "unlock_features": ["개인적인 이야기 공유"],
        "title": "님"
    },
    (41, 60): {
        "level": "친구",
        "description": "편안하고 자연스러운 대화",
        "speech_pattern": "가끔 반말, 농담도 함",
        "unlock_features": ["고민상담", "일상 이야기"],
        "title": "씨" 
    },
    (61, 80): {
        "level": "절친",
        "description": "깊은 신뢰와 애정",
        "speech_pattern": "자연스러운 반말, 애교도 부림",
        "unlock_features": ["비밀 이야기", "특별한 호칭"],
        "title": ""
    },
    (81, 100): {
        "level": "특별한사람", 
        "description": "최고 단계의 친밀감",
        "speech_pattern": "완전히 편안함, 때로는 부끄러워함",
        "unlock_features": ["연인 모드", "특별 이벤트"],
        "title": ""
    }
}

# 호감도 변화 트리거
AFFECTION_TRIGGERS = {
    # 증가 요소
    "daily_chat": 1,           # 매일 대화
    "long_conversation": 2,     # 긴 대화 (10분 이상)
    "compliment": 3,           # 칭찬
    "remember_details": 5,      # 카오루코 정보 기억
    "gift_mention": 7,         # 선물 언급
    "romantic_gesture": 10,     # 로맨틱한 행동
    "special_occasion": 15,     # 특별한 날 기념
    
    # 감소 요소
    "rude_behavior": -5,        # 무례한 행동
    "ignore_long_time": -3,     # 오랫동안 무시 (하루 이상)
    "inappropriate_content": -10, # 부적절한 내용
    "break_promise": -8,        # 약속 위반
    "harsh_words": -6,          # 상처주는 말
}


class AffectionManager:
    """호감도를 관리하는 클래스"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_affection(self, user_name: str) -> Tuple[int, str, int]:
        """
        사용자의 호감도 정보를 가져옵니다
        
        Returns:
            (affection_level, relationship_stage, days_since_first_met)
        """
        from models import UserAffection
        
        affection_record = self.db.query(UserAffection).filter(
            UserAffection.user_name == user_name
        ).first()
        
        if not affection_record:
            # 새 사용자인 경우 초기화
            return self.initialize_user_affection(user_name)
        
        # 첫 만남부터 경과일 계산
        days_since_first_met = (date.today() - affection_record.first_met_date).days
        relationship_stage = self.get_relationship_stage(affection_record.affection_level)
        
        return affection_record.affection_level, relationship_stage, days_since_first_met
    
    def initialize_user_affection(self, user_name: str) -> Tuple[int, str, int]:
        """새 사용자의 호감도를 초기화합니다"""
        from models import UserAffection
        
        new_affection = UserAffection(
            user_name=user_name,
            affection_level=0,  # 0부터 시작
            total_conversations=0,
            first_met_date=date.today()
        )
        
        self.db.add(new_affection)
        self.db.commit()
        
        return 0, "낯선사람", 0
    
    def update_affection(self, user_name: str, trigger: str, 
                        multiplier: float = 1.0) -> Tuple[int, int, bool]:
        """
        트리거에 따라 호감도를 업데이트합니다
        
        Returns:
            (new_affection_level, affection_change, level_up_occurred)
        """
        from models import UserAffection, EmotionHistory
        
        current_level, _, _ = self.get_user_affection(user_name)
        
        # 호감도 변화량 계산
        base_change = AFFECTION_TRIGGERS.get(trigger, 0)
        affection_change = math.ceil(base_change * multiplier)
        
        # 새로운 호감도 계산 (-100 ~ 100 사이로 제한)
        new_affection_level = max(-100, min(100, current_level + affection_change))

        # 레벨 변화 여부 확인 (증가/감소 모두 감지)
        old_stage = self.get_relationship_stage(current_level)
        new_stage = self.get_relationship_stage(new_affection_level)
        level_up_occurred = (old_stage != new_stage)
        
        # 데이터베이스 업데이트
        affection_record = self.db.query(UserAffection).filter(
            UserAffection.user_name == user_name
        ).first()
        
        if affection_record:
            affection_record.affection_level = new_affection_level
            affection_record.total_conversations += 1
            affection_record.last_interaction = datetime.now()
            
            # 호감도 변화 기록은 EmotionAnalyzer에서 처리
            # emotion_history는 새로운 모델로 EmotionAnalyzer가 담당
            pass
        
        self.db.commit()
        
        return new_affection_level, affection_change, level_up_occurred
    
    def get_relationship_stage(self, affection_level: int) -> str:
        """호감도에 따른 관계 단계를 반환합니다"""
        for (min_val, max_val), stage_info in AFFECTION_LEVELS.items():
            if min_val <= affection_level <= max_val:
                return stage_info["level"]
        return "낯선사람"
    
    def get_stage_info(self, affection_level: int) -> Dict:
        """호감도에 따른 단계 정보를 반환합니다"""
        for (min_val, max_val), stage_info in AFFECTION_LEVELS.items():
            if min_val <= affection_level <= max_val:
                return stage_info
        return AFFECTION_LEVELS[(0, 20)]  # 기본값
    
    def get_title_for_user(self, user_name: str, affection_level: int) -> str:
        """호감도에 따른 호칭을 반환합니다"""
        stage_info = self.get_stage_info(affection_level)
        title = stage_info.get("title", "님")
        
        if title:
            return f"{user_name}{title}"
        else:
            # 높은 호감도에서는 이름만 부르거나 특별한 호칭
            if affection_level >= 80:
                return user_name  # 이름만
            elif affection_level >= 60:
                return f"{user_name}아" if user_name.endswith(('ㄱ', 'ㄴ', 'ㄷ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅅ', 'ㅇ', 'ㅈ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ')) else f"{user_name}야"
        
        return f"{user_name}{title}"
    
    def check_daily_bonus(self, user_name: str) -> int:
        """일일 보너스 호감도를 확인하고 지급합니다"""
        from models import UserAffection
        
        affection_record = self.db.query(UserAffection).filter(
            UserAffection.user_name == user_name
        ).first()
        
        if not affection_record:
            return 0
        
        # 마지막 상호작용이 어제 이전인지 확인
        if affection_record.last_interaction.date() < date.today():
            return self.update_affection(user_name, "daily_chat")[1]
        
        return 0
    
    def get_level_up_message(self, new_stage: str) -> str:
        """레벨업 시 표시할 메시지를 생성합니다"""
        messages = {
            "지인": "어... 조금씩 친해지는 것 같아요. 기쁘네요! 😊",
            "친구": "이제 좀 더 편하게 얘기할 수 있을 것 같아요~ 친구가 된 것 같아서 기뻐요!",
            "절친": "우리 정말 친해졌네요! 이제 뭐든지 얘기할 수 있을 것 같아요~ 💕",
            "특별한사람": "저... 저에게 이렇게 특별한 사람이 생길 줄 몰랐어요... 정말... 고마워요... 💖"
        }
        return messages.get(new_stage, "관계가 발전했어요!")
    
    def get_affection_progress_percentage(self, affection_level: int) -> float:
        """현재 단계에서의 진행률을 퍼센트로 반환합니다"""
        # 음수 구간(멀어진사람)은 절대값 기준으로 진행률을 표시
        if affection_level < 0:
            return (abs(affection_level) / 100.0) * 100.0

        for (min_val, max_val), _ in AFFECTION_LEVELS.items():
            if min_val <= affection_level <= max_val and min_val >= 0:
                if max_val == min_val:
                    return 100.0
                return ((affection_level - min_val) / (max_val - min_val)) * 100
        return 0.0
    
    def get_all_stages(self) -> Dict:
        """모든 관계 단계 정보를 반환합니다"""
        return AFFECTION_LEVELS