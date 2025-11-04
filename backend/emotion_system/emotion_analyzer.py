"""
감정 분석 시스템 (Emotion System Stage 2)
실시간 대화 내용 분석을 통한 카오루코의 감정 상태 추출
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Tuple, Optional
from sqlalchemy.orm import Session
import google.generativeai as genai

class EmotionAnalyzer:
    """
    카오루코의 감정을 실시간으로 분석하는 클래스
    6가지 핵심 감정: 수줍음, 기쁨, 슬픔, 화남, 놀람, 설렘
    """
    
    # 6가지 핵심 감정 정의
    EMOTIONS = {
        "수줍음": {
            "emoji": "😊",
            "color": "#ffb3d9",
            "description": "부끄러워하거나 수줍어하는 상태",
            "keywords": ["부끄", "수줍", "얼굴", "빨개", "어색", "쑥스러", "창피"]
        },
        "기쁨": {
            "emoji": "😄", 
            "color": "#ffd700",
            "description": "행복하고 즐거운 상태",
            "keywords": ["기쁘", "행복", "즐거", "웃", "좋", "반가", "신나"]
        },
        "슬픔": {
            "emoji": "😢",
            "color": "#87ceeb", 
            "description": "슬프거나 우울한 상태",
            "keywords": ["슬프", "우울", "눈물", "울", "안타까", "아쉬", "힘들"]
        },
        "화남": {
            "emoji": "😠",
            "color": "#ff6b6b",
            "description": "화나거나 짜증나는 상태", 
            "keywords": ["화", "짜증", "화나", "속상", "억울", "빡", "열받"]
        },
        "놀람": {
            "emoji": "😲",
            "color": "#98fb98",
            "description": "놀라거나 당황한 상태",
            "keywords": ["놀라", "깜짝", "어머", "헉", "와", "당황", "어떡해"]
        },
        "설렘": {
            "emoji": "💕",
            "color": "#ff69b4", 
            "description": "설레거나 두근거리는 상태",
            "keywords": ["설레", "두근", "떨려", "궁금", "기대", "간지럽", "따뜻"]
        }
    }
    
    def __init__(self, db_session: Session, genai_model):
        self.db = db_session
        self.model = genai_model
        self.current_emotion = "수줍음"  # 기본 감정
        self.emotion_intensity = 5  # 1-10 강도
        self.emotion_history = []
    
    def analyze_emotion(self, user_message: str, bot_reply: str, user_name: str) -> Dict:
        """
        대화 내용을 분석하여 카오루코의 감정 상태를 추출
        
        Args:
            user_message: 사용자의 메시지
            bot_reply: 카오루코의 답변
            user_name: 사용자 이름
            
        Returns:
            감정 분석 결과 딕셔너리
        """
        try:
            # Gemini API를 이용한 감정 분석
            emotion_prompt = self._create_emotion_prompt(user_message, bot_reply, user_name)
            
            response = self.model.generate_content(emotion_prompt)
            emotion_data = self._parse_emotion_response(response.text)
            
            # 감정 히스토리에 저장
            self._save_emotion_history(user_name, emotion_data)
            
            # 현재 감정 상태 업데이트
            self.current_emotion = emotion_data.get("emotion", "수줍음")
            self.emotion_intensity = emotion_data.get("intensity", 5)
            
            return {
                "emotion": self.current_emotion,
                "intensity": self.emotion_intensity,
                "emoji": self.EMOTIONS[self.current_emotion]["emoji"],
                "color": self.EMOTIONS[self.current_emotion]["color"],
                "reason": emotion_data.get("reason", ""),
                "confidence": emotion_data.get("confidence", 0.8)
            }
            
        except Exception as e:
            print(f"감정 분석 오류: {e}")
            return self._get_default_emotion()
    
    def _create_emotion_prompt(self, user_message: str, bot_reply: str, user_name: str) -> str:
        """감정 분석을 위한 프롬프트 생성"""
        
        emotions_list = ", ".join([f"{name}({data['emoji']})" for name, data in self.EMOTIONS.items()])
        
        prompt = f"""
다음은 와구리 카오루코(수줍은 고등학생 캐릭터)와 {user_name}님의 대화입니다.

사용자 메시지: "{user_message}"
카오루코 답변: "{bot_reply}"

카오루코의 현재 감정을 다음 6가지 중에서 분석해주세요:
{emotions_list}

다음 JSON 형식으로만 답변해주세요:
{{
    "emotion": "감정이름",
    "intensity": 강도(1-10),
    "reason": "감정선택이유",
    "confidence": 확신도(0.0-1.0)
}}

카오루코는 단데레 타입으로 쉽게 부끄러워하고, 칭찬받으면 수줍어하며, 
친밀해질수록 설레는 반응을 보입니다.
"""
        return prompt
    
    def _parse_emotion_response(self, response_text: str) -> Dict:
        """Gemini 응답에서 감정 정보 추출"""
        try:
            # JSON 부분만 추출
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                emotion_data = json.loads(json_str)
                
                # 유효성 검사
                if emotion_data.get("emotion") not in self.EMOTIONS:
                    emotion_data["emotion"] = "수줍음"
                
                emotion_data["intensity"] = max(1, min(10, emotion_data.get("intensity", 5)))
                emotion_data["confidence"] = max(0.0, min(1.0, emotion_data.get("confidence", 0.8)))
                
                return emotion_data
            
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"감정 파싱 오류: {e}")
        
        # 기본값 반환
        return {
            "emotion": "수줍음",
            "intensity": 5,
            "reason": "기본 감정",
            "confidence": 0.5
        }
    
    def _save_emotion_history(self, user_name: str, emotion_data: Dict):
        """감정 히스토리를 데이터베이스에 저장"""
        try:
            from models import EmotionHistory
            
            emotion_entry = EmotionHistory(
                user_name=user_name,
                emotion=emotion_data["emotion"],
                intensity=emotion_data["intensity"],
                reason=emotion_data.get("reason", ""),
                confidence=emotion_data.get("confidence", 0.8),
                timestamp=datetime.now()
            )
            
            self.db.add(emotion_entry)
            self.db.commit()
            
            # 메모리에도 저장 (최근 10개만)
            self.emotion_history.append({
                "emotion": emotion_data["emotion"],
                "intensity": emotion_data["intensity"],
                "timestamp": datetime.now()
            })
            
            if len(self.emotion_history) > 10:
                self.emotion_history.pop(0)
                
        except Exception as e:
            print(f"감정 히스토리 저장 오류: {e}")
    
    def _get_default_emotion(self) -> Dict:
        """기본 감정 상태 반환"""
        return {
            "emotion": "수줍음",
            "intensity": 5,
            "emoji": "😊",
            "color": "#ffb3d9", 
            "reason": "기본 상태",
            "confidence": 0.5
        }
    
    def get_emotion_stats(self, user_name: str) -> Dict:
        """사용자별 감정 통계 반환"""
        try:
            from models import EmotionHistory
            from sqlalchemy import func
            
            # 최근 감정 분포 계산
            recent_emotions = self.db.query(EmotionHistory.emotion, func.count(EmotionHistory.emotion)) \
                .filter(EmotionHistory.user_name == user_name) \
                .group_by(EmotionHistory.emotion) \
                .all()
            
            emotion_counts = {emotion: count for emotion, count in recent_emotions}
            total_count = sum(emotion_counts.values())
            
            if total_count == 0:
                return {"dominant_emotion": "수줍음", "emotion_distribution": {}}
            
            # 가장 많이 나타난 감정
            dominant_emotion = max(emotion_counts, key=emotion_counts.get)
            
            # 감정 분포 퍼센트로 변환
            emotion_distribution = {
                emotion: round((count / total_count) * 100, 1)
                for emotion, count in emotion_counts.items()
            }
            
            return {
                "dominant_emotion": dominant_emotion,
                "emotion_distribution": emotion_distribution,
                "total_interactions": total_count
            }
            
        except Exception as e:
            print(f"감정 통계 오류: {e}")
            return {"dominant_emotion": "수줍음", "emotion_distribution": {}}
    
    def get_current_emotion(self) -> Dict:
        """현재 감정 상태 반환"""
        return {
            "emotion": self.current_emotion,
            "intensity": self.emotion_intensity,
            "emoji": self.EMOTIONS[self.current_emotion]["emoji"],
            "color": self.EMOTIONS[self.current_emotion]["color"],
            "description": self.EMOTIONS[self.current_emotion]["description"]
        }