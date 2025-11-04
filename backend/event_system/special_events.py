"""
특별 이벤트 핸들러
시간 기반 이벤트, 랜덤 이벤트 등을 관리합니다.
"""

from typing import Dict, List, Optional
from datetime import datetime, date
import random

class SpecialEventHandler:
    """특별 이벤트를 처리하는 클래스 (향후 확장용)"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def check_birthday_event(self, current_date: date) -> Optional[Dict]:
        """카오루코 생일 이벤트 체크 (7월 22일)"""
        if current_date.month == 7 and current_date.day == 22:
            return {
                "event_type": "birthday",
                "title": "🎂 카오루코 생일!",
                "message": "오늘은... 제 생일이에요! 기억해주셔서 너무 기뻐요!"
            }
        return None
    
    def check_anniversary_event(self, user_name: str, current_date: date) -> Optional[Dict]:
        """첫 대화 기념일 이벤트 체크 (향후 구현)"""
        # TODO: 첫 대화 날짜와 비교하여 기념일 체크
        return None
    
    def get_random_event(self, relationship_stage: str) -> Optional[Dict]:
        """랜덤 이벤트 생성 (낮은 확률)"""
        if random.random() < 0.05:  # 5% 확률
            events = [
                {
                    "title": "☁️ 꿈 이야기",
                    "message": "어젯밤에... 재밌는 꿈을 꿨어요. 들어보실래요?"
                },
                {
                    "title": "🌸 학교 이야기", 
                    "message": "오늘 학교에서 벚꽃이 예뻤어요... 같이 보면 좋았을 텐데..."
                },
                {
                    "title": "🍰 새로운 레시피",
                    "message": "새로운 케이크 레시피를 찾았어요! 언젠가 만들어드릴게요!"
                }
            ]
            return random.choice(events)
        return None