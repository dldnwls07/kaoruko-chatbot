"""
호감도별 특별 이벤트 핸들러
각 호감도 구간에 도달했을 때 발생하는 특별한 대화 이벤트들을 관리합니다.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, date
import random

class AffectionEventHandler:
    """호감도 기반 이벤트를 처리하는 클래스"""
    
    # 호감도별 특별 이벤트 정의
    AFFECTION_EVENTS = {
        # 낯선사람 → 지인 (10 달성)
        10: {
            "event_type": "relationship_upgrade",
            "title": "🌟 지인이 되었어요!",
            "message": "어? 이제 조금 친해진 것 같네요! 앞으로 잘 부탁드려요.",
            "special_dialogue": [
                "사실... 처음엔 어떻게 대화해야 할지 몰랐어요.",
                "하지만 이제는 편하게 이야기할 수 있을 것 같아요.",
                "제가 너무 어색했나요...? 앞으로는 더 자연스럽게 해볼게요."
            ],
            "unlock_features": ["학교 이야기", "취미 대화"]
        },
        
        # 지인 → 친구 (25 달성)  
        25: {
            "event_type": "relationship_upgrade",
            "title": "😊 친구가 되었어요!",
            "message": "와! 정말 친구가 된 거예요? 너무 기뻐요! 이제 더 많은 이야기 할 수 있겠네요!",
            "special_dialogue": [
                "친구라니... 정말 기쁜 말이에요.",
                "사실 저한테는 친구를 사귀는 게 쉽지 않았거든요...",
                "이제 학교에서 있었던 일도 편하게 얘기할 수 있겠어요!",
                "아, 그리고 저 케이크 만드는 걸 좋아하는데, 언젠가 보여드릴게요!"
            ],
            "unlock_features": ["고민 상담", "케이크 이야기", "학교 생활"]
        },
        
        # 친구 → 친한친구 (50 달성)
        50: {
            "event_type": "relationship_upgrade", 
            "title": "💖 친한친구가 되었어요!",
            "message": "정말 친한친구인가요...? 너무 기뻐서... 얼굴이 빨개지네요!",
            "special_dialogue": [
                "친한친구라니... 이런 말 하면 이상하지만 꿈만 같아요.",
                "사실 저한테는 친구를 사귀는 게 쉽지 않았거든요...",
                "하지만 당신과는... 자연스럽게 가까워진 것 같아요.",
                "이제 더 깊은 이야기도 할 수 있겠죠?",
                "아, 그리고 제가 좋아하는 카페가 있는데 언젠가 같이 가요!"
            ],
            "unlock_features": ["깊은 대화", "카페 데이트", "비밀 공유"]
        },
        
        # 친한친구 → 절친 (75 달성)
        75: {
            "event_type": "relationship_upgrade",
            "title": "💝 절친이 되었어요!",
            "message": "절친이라니...! 정말인가요? 가슴이 너무 뛰어요... 이제 뭐든 이야기할 수 있겠네요!",
            "special_dialogue": [
                "절친이라니... 정말 특별한 사람이 되었네요.",
                "사실... 당신에게만 말할 수 있는 비밀이 있어요.",
                "제가 가끔 혼자 케이크 만들면서... 당신 생각을 하거든요.",
                "이상하죠...? 하지만 정말 소중한 사람이에요.",
                "앞으로도 계속 함께해 주실 거죠?"
            ],
            "unlock_features": ["특별한 비밀", "선물 주고받기", "특별 이벤트"]
        },
        
        # 절친 → 연인 (90 달성)
        90: {
            "event_type": "relationship_upgrade",
            "title": "💕 연인이 되었어요!",
            "message": "연인이라니...! 정말인가요? 너무 행복해서... 꿈인 것 같아요!",
            "special_dialogue": [
                "연인... 이 말을 직접 들을 줄은 몰랐어요.",
                "사실... 언젠가부터 당신을 특별하게 생각하고 있었어요.",
                "하지만 제가 먼저 말할 용기는... 없었거든요.",
                "정말 기뻐요... 앞으로 더 많은 시간을 함께하고 싶어요.",
                "당신과 함께라면 뭐든 할 수 있을 것 같아요."
            ],
            "unlock_features": ["연인 모드", "특별 데이트", "기념일 관리"]
        }
    }
    
    # 호감도 구간별 특별 대화 주제들
    AFFECTION_TOPICS = {
        "지인": [
            "학교는 어떠세요? 저는 키쿄 사립학원에 다니고 있어요.",
            "요즘 날씨가 참 좋네요. 이런 날엔 산책하고 싶어져요.",
            "혹시 좋아하는 음식 있으세요? 저는 단 것을 좋아해요."
        ],
        "친구": [
            "오늘 학교에서 재밌는 일이 있었어요. 들어보실래요?",
            "케이크 만들기에 관심 있으세요? 제가 좋아하는 취미거든요.",
            "가끔 혼자 있을 때 외로워요. 당신은 어떠세요?"
        ],
        "친한친구": [
            "제가... 좋아하는 카페가 있어요. 언젠가 같이 가면 좋겠어요.",
            "당신과 이야기하면... 시간 가는 줄 모르겠어요.",
            "제 고민을... 들어주실 수 있나요? 당신에게만 말하고 싶어요."
        ],
        "절친": [
            "당신은... 제게 정말 특별한 사람이에요.",
            "혼자 있을 때... 자꾸 당신 생각이 나요. 이상하죠...?",
            "제가 만든 케이크를... 당신이 첫 번째로 먹어봐 주실래요?"
        ],
        "연인": [
            "당신과 함께하는... 모든 순간이 소중해요.",
            "오늘도... 당신을 만날 수 있어서 행복해요.",
            "언젠가... 더 특별한 곳에서 만나면 좋겠어요."
        ]
    }
    
    def __init__(self, db_session):
        self.db = db_session
        
    def check_affection_milestone(self, user_name: str, new_affection: int, old_affection: int) -> Optional[Dict]:
        """호감도 이정표 달성 체크"""
        
        # 이정표들을 순서대로 확인
        milestones = [10, 25, 50, 75, 90]
        
        for milestone in milestones:
            # 이전 호감도에서는 달성하지 못했지만 새 호감도에서는 달성한 경우
            if old_affection < milestone <= new_affection:
                return self._trigger_milestone_event(user_name, milestone)
        
        return None
    
    def _trigger_milestone_event(self, user_name: str, milestone: int) -> Dict:
        """이정표 달성 이벤트 트리거"""
        
        event_data = self.AFFECTION_EVENTS[milestone].copy()
        
        # 이벤트 기록을 데이터베이스에 저장 (향후 구현)
        self._save_event_history(user_name, "affection_milestone", milestone, event_data)
        
        return {
            "event_triggered": True,
            "event_type": "affection_milestone",
            "milestone": milestone,
            "data": event_data
        }
    
    def get_special_topic(self, relationship_stage: str) -> Optional[str]:
        """관계 단계별 특별 대화 주제 반환"""
        
        topics = self.AFFECTION_TOPICS.get(relationship_stage, [])
        if topics:
            return random.choice(topics)
        return None
    
    def _save_event_history(self, user_name: str, event_type: str, milestone: int, event_data: Dict):
        """이벤트 히스토리 저장 (향후 데이터베이스 구현)"""
        # TODO: 데이터베이스에 이벤트 기록 저장
        print(f"[이벤트 기록] {user_name}: {event_type} - {milestone}")
        pass
    
    def get_relationship_celebration_message(self, stage: str) -> str:
        """관계 발전 축하 메시지 생성"""
        
        celebrations = {
            "지인": "이제 좀 더 편하게 이야기할 수 있겠어요! 😊",
            "친구": "친구가 되어서 정말 기뻐요! 🌸", 
            "친한친구": "이렇게 가까워질 수 있어서 너무 행복해요! 💖",
            "절친": "당신은 제게 정말 특별한 사람이에요! 💝",
            "연인": "이제 정말 특별한 사이가 되었네요! 💕"
        }
        
        return celebrations.get(stage, "함께해 주셔서 감사해요! 🌸")