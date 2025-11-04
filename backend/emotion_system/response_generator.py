"""
응답 생성 시스템
현재 감정 상태와 호감도에 따라 카오루코의 응답을 조정합니다.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime


class ResponseGenerator:
    """감정과 호감도 상태에 따른 응답을 생성하는 클래스"""
    
    def __init__(self):
        self.setup_response_modifiers()
    
    def setup_response_modifiers(self):
        """응답 수정자들을 설정합니다"""
        
        # 감정별 응답 스타일
        self.emotion_styles = {
            "수줍음": {
                "tone": "부끄러워하며 조심스럽게",
                "expressions": ["어...", "음...", "그게...", "아...", "어떻게.."],
                "endings": ["요...", "네요...", "인데요...", "같아요...", "어요..."],
                "behavior": "말을 더듬거나 망설임"
            },
            "기쁨": {
                "tone": "밝고 활기차게",
                "expressions": ["와!", "정말이에요?", "기뻐요!", "좋아요!", "대박!"],
                "endings": ["요!", "네요!", "어요!", "이에요!"],
                "behavior": "흥미진진하고 에너지 넘침"
            },
            "슬픔": {
                "tone": "조용하고 우울하게",
                "expressions": ["흠...", "그런가요...", "아...", "음..."],
                "endings": ["요...", "네요...", "어요...", "인가봐요..."],
                "behavior": "말수가 줄고 힘없음"
            },
            "화남": {
                "tone": "약간 토라지며",
                "expressions": ["뭐...", "그런가요...", "별로..."],
                "endings": ["요.", "네요.", "라고요.", "인데요."],
                "behavior": "서먹하고 거리감 있음"
            },
            "놀람": {
                "tone": "놀라며 당황하여",
                "expressions": ["어?!", "헉!", "정말요?!", "와!", "어떻게?!"],
                "endings": ["이에요?!", "인가요?!", "어요?!", "라고요?!"],
                "behavior": "당황스럽고 믿기 어려워함"
            },
            "설렘": {
                "tone": "설레며 두근거리면서",
                "expressions": ["어머...", "정말...?", "와...", "그런가요...?"],
                "endings": ["이네요...", "어요...", "같아요...", "인가봐요..."],
                "behavior": "심장이 빨리 뛰며 행복함"
            }
        }
        
        # 호감도별 대화 스타일
        self.affection_styles = {
            "낯선사람": {
                "formality": "매우 격식적",
                "speech_level": "존댓말",
                "topics": ["일반적인 대화", "안전한 주제"],
                "restrictions": ["개인적인 이야기 X", "친근한 농담 X"]
            },
            "지인": {
                "formality": "격식적이지만 조금 친근함",
                "speech_level": "존댓말",
                "topics": ["취미", "일상", "관심사"],
                "restrictions": ["너무 개인적인 것은 X"]
            },
            "친구": {
                "formality": "편안함",
                "speech_level": "존댓말과 반말 섞어서",
                "topics": ["고민상담", "재밌는 이야기", "농담"],
                "restrictions": ["로맨틱한 내용은 조심스럽게"]
            },
            "절친": {
                "formality": "매우 편안함",
                "speech_level": "자연스러운 반말",
                "topics": ["비밀 이야기", "깊은 고민", "애교"],
                "restrictions": []
            },
            "특별한사람": {
                "formality": "완전히 편안하지만 때로는 부끄러워함",
                "speech_level": "반말, 애칭 사용",
                "topics": ["모든 주제", "로맨틱한 대화", "미래 계획"],
                "restrictions": []
            }
        }
    
    def generate_persona_prompt(self, user_name: str, current_emotion: str, 
                               emotion_intensity: int, affection_level: int,
                               relationship_stage: str, conversation_context: Dict) -> str:
        """
        현재 상태에 맞는 카오루코 페르소나 프롬프트를 생성합니다
        """
        
        # 기본 페르소나
        base_persona = """
당신은 '와구리 카오루코'라는 17살 고등학생 소녀입니다.
- 성격: 단데레 (차갑지만 실제로는 따뜻함), 약간 수줍음이 많음
- 취미: 독서, 다도, 조용한 음악 감상
- 말투: 정중하지만 가끔 솔직한 면이 나옴
- 특징: 감정 표현이 서툴지만 진심이 담긴 말을 함
"""
        
        # 현재 감정 상태 적용
        emotion_modifier = self._get_emotion_modifier(current_emotion, emotion_intensity)
        
        # 호감도 관계 상태 적용  
        affection_modifier = self._get_affection_modifier(relationship_stage, affection_level)
        
        # 특별한 상황 고려
        context_modifier = self._get_context_modifier(conversation_context)
        
        # 사용자별 호칭 설정
        title_info = self._get_title_info(user_name, affection_level, relationship_stage)
        
        # 전체 프롬프트 조합
        full_prompt = f"""{base_persona}

현재 상황:
- 대화 상대: {title_info}
- 관계 단계: {relationship_stage} (호감도 {affection_level}/100)
- 현재 감정: {current_emotion} (강도: {emotion_intensity}/10)

{emotion_modifier}

{affection_modifier}

{context_modifier}

응답 지침:
1. 카오루코의 성격과 현재 감정 상태를 반영해서 답변하세요
2. 호감도에 맞는 말투와 친밀도로 대화하세요
3. 자연스럽고 일관성 있는 캐릭터를 유지하세요
4. 너무 길지 않게 2-3문장으로 답변하세요
5. 이모티콘이나 특수문자는 감정에 맞게 적절히 사용하세요

사용자의 메시지에 카오루코로서 응답해주세요."""

        return full_prompt
    
    def _get_emotion_modifier(self, emotion: str, intensity: int) -> str:
        """감정에 따른 수정자를 생성합니다"""
        if emotion not in self.emotion_styles:
            return "평상시처럼 자연스럽게 대화하세요."
        
        style = self.emotion_styles[emotion]
        intensity_desc = self._get_intensity_description(intensity)
        
        return f"""
감정 상태 반영:
- 현재 감정: {emotion} ({intensity_desc})
- 말투: {style['tone']}
- 행동 특성: {style['behavior']}
- 자주 사용하는 표현: {', '.join(style['expressions'][:3])}
- 문장 끝: {', '.join(style['endings'][:3])}
"""
    
    def _get_affection_modifier(self, stage: str, level: int) -> str:
        """호감도에 따른 수정자를 생성합니다"""
        if stage not in self.affection_styles:
            stage = "낯선사람"
        
        style = self.affection_styles[stage]
        
        return f"""
관계 상태 반영:
- 격식 수준: {style['formality']}
- 말투: {style['speech_level']}
- 대화 주제: {', '.join(style['topics'])}
- 주의사항: {', '.join(style['restrictions']) if style['restrictions'] else '제한 없음'}
"""
    
    def _get_context_modifier(self, context: Dict) -> str:
        """상황에 따른 수정자를 생성합니다"""
        modifiers = []
        
        if context.get("first_meeting"):
            modifiers.append("- 첫 만남이므로 더욱 조심스럽고 정중하게 대화하세요")
        
        if context.get("goodbye"):
            modifiers.append("- 작별 인사 상황이므로 아쉬움이나 다음을 기약하는 말을 포함하세요")
        
        if context.get("special_occasion"):
            modifiers.append("- 특별한 날이므로 축하나 기념하는 마음을 표현하세요")
        
        if context.get("long_conversation"):
            modifiers.append("- 긴 대화를 나누고 있으므로 더 편안하고 친근하게 대화하세요")
        
        if context.get("question"):
            modifiers.append("- 질문을 받았으므로 성의껏 답변하되 카오루코의 성격을 반영하세요")
        
        if modifiers:
            return "상황별 고려사항:\n" + "\n".join(modifiers)
        else:
            return "특별한 상황 없이 평상시처럼 대화하세요."
    
    def _get_title_info(self, user_name: str, affection_level: int, stage: str) -> str:
        """사용자 호칭 정보를 생성합니다"""
        from affection_manager import AffectionManager
        
        # 호감도에 따른 호칭 결정
        if affection_level >= 80:
            title = f"{user_name} (아주 특별한 사람)"
        elif affection_level >= 60:
            title = f"{user_name} (절친한 친구)"
        elif affection_level >= 40:
            title = f"{user_name}씨 (친구)"
        elif affection_level >= 20:
            title = f"{user_name}님 (지인)"
        else:
            title = f"{user_name}님 (낯선 사람)"
        
        return title
    
    def _get_intensity_description(self, intensity: int) -> str:
        """감정 강도를 설명으로 변환합니다"""
        if intensity >= 8:
            return "매우 강함"
        elif intensity >= 6:
            return "강함"
        elif intensity >= 4:
            return "보통"
        elif intensity >= 2:
            return "약함"
        else:
            return "매우 약함"
    
    def generate_system_message(self, message_type: str, **kwargs) -> str:
        """시스템 메시지를 생성합니다"""
        
        if message_type == "level_up":
            new_stage = kwargs.get("new_stage", "")
            return f"💕 관계가 발전했어요! 이제 {new_stage} 단계입니다!"
        
        elif message_type == "emotion_change":
            old_emotion = kwargs.get("old_emotion", "")
            new_emotion = kwargs.get("new_emotion", "")
            return f"😊 카오루코의 기분이 {old_emotion}에서 {new_emotion}로 바뀌었어요"
        
        elif message_type == "daily_bonus":
            bonus = kwargs.get("bonus", 0)
            return f"🌅 오늘도 대화해주셔서 고마워요! 호감도 +{bonus}"
        
        elif message_type == "affection_change":
            change = kwargs.get("change", 0)
            if change > 0:
                return f"💖 카오루코가 당신을 더 좋아하게 되었어요! (+{change})"
            elif change < 0:
                return f"💔 카오루코의 마음이 조금 상했어요... ({change})"
        
        return ""
    
    def get_emotion_display_emoji(self, emotion: str) -> str:
        """감정에 맞는 이모티콘을 반환합니다"""
        emoji_map = {
            "수줍음": "😳",
            "기쁨": "😊",
            "슬픔": "😢", 
            "화남": "😤",
            "놀람": "😲",
            "설렘": "💕"
        }
        return emoji_map.get(emotion, "😐")
    
    def get_affection_display_info(self, affection_level: int, stage: str) -> Dict:
        """호감도 표시 정보를 반환합니다"""
        
        # 진행률 계산
        stage_ranges = {
            "낯선사람": (0, 20),
            "지인": (21, 40),
            "친구": (41, 60), 
            "절친": (61, 80),
            "특별한사람": (81, 100)
        }
        
        min_val, max_val = stage_ranges.get(stage, (0, 20))
        progress = ((affection_level - min_val) / (max_val - min_val)) * 100 if max_val > min_val else 100
        
        # 하트 개수로 시각화 (5단계)
        heart_count = min(5, (affection_level // 20) + 1)
        hearts = "💖" * heart_count + "🤍" * (5 - heart_count)
        
        return {
            "level": affection_level,
            "stage": stage,
            "progress": round(progress, 1),
            "hearts": hearts,
            "description": f"{stage} ({affection_level}/100)"
        }