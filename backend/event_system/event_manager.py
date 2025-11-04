"""
이벤트 시스템 매니저
모든 이벤트를 총괄 관리하고 적절한 타이밍에 이벤트를 트리거합니다.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime, date
from .affection_events import AffectionEventHandler

class EventManager:
    """전체 이벤트 시스템을 관리하는 메인 클래스"""
    
    def __init__(self, db_session):
        self.db = db_session
        self.affection_events = AffectionEventHandler(db_session)
        
    def process_conversation_events(self, user_name: str, message: str, response: str, 
                                  emotion_data: Dict, affection_data: Dict) -> List[Dict]:
        """대화 후 발생할 수 있는 모든 이벤트를 처리"""
        
        events = []
        
        # 1. 호감도 이정표 이벤트 체크
        if affection_data.get('affection_change', 0) > 0:
            old_affection = affection_data.get('old_affection', 0)
            new_affection = affection_data.get('current_affection', 0)
            
            milestone_event = self.affection_events.check_affection_milestone(
                user_name, new_affection, old_affection
            )
            
            if milestone_event:
                events.append(milestone_event)
        
        # 2. 특별 대화 주제 제안 (낮은 확률로)
        relationship_stage = affection_data.get('relationship_stage', '낯선사람')
        if self._should_suggest_special_topic():
            special_topic = self.affection_events.get_special_topic(relationship_stage)
            if special_topic:
                events.append({
                    "event_triggered": True,
                    "event_type": "special_topic",
                    "data": {
                        "topic": special_topic,
                        "message": f"아, 그런데... {special_topic}"
                    }
                })
        
        # 3. 감정 기반 특별 반응 (향후 구현)
        # emotion_event = self._check_emotion_events(emotion_data)
        
        return events
    
    def _should_suggest_special_topic(self) -> bool:
        """특별 주제를 제안할지 확률적으로 결정 (10% 확률)"""
        import random
        return random.random() < 0.1
    
    def get_welcome_message_for_relationship(self, relationship_stage: str, user_name: str) -> Optional[str]:
        """관계 단계별 환영 메시지"""
        
        welcome_messages = {
            "낯선사람": f"어... 안녕하세요, {user_name}님... 처음 뵙겠습니다.",
            "지인": f"안녕하세요 {user_name}님! 오늘도 만나뵙게 되어서... 기뻐요.",
            "친구": f"{user_name}님! 안녕하세요~ 오늘 하루는 어떠셨어요?",
            "친한친구": f"{user_name}님! 오늘도 만날 수 있어서 너무 기뻐요! 😊",
            "절친": f"{user_name}님... 오늘도 와주셔서 고마워요. 정말 소중한 시간이에요.",
            "연인": f"{user_name}님... 오늘도 만날 수 있어서 행복해요. 보고 싶었어요... 💕"
        }
        
        return welcome_messages.get(relationship_stage)
    
    def format_event_for_ui(self, event: Dict) -> Dict:
        """이벤트를 UI에서 표시할 형태로 포맷팅"""
        
        if event["event_type"] == "affection_milestone":
            return {
                "type": "milestone_achievement",
                "title": event["data"]["title"],
                "message": event["data"]["message"],
                "special_dialogue": event["data"]["special_dialogue"],
                "unlock_features": event["data"].get("unlock_features", []),
                "celebration": True
            }
        
        elif event["event_type"] == "special_topic":
            return {
                "type": "special_conversation",
                "message": event["data"]["message"],
                "topic": event["data"]["topic"]
            }
        
        return event