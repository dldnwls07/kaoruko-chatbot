"""
메시지 트리거 분석 시스템
사용자의 메시지를 분석해서 감정과 호감도 변화 트리거를 감지합니다.
"""

import re
from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta


class TriggerDetector:
    """사용자 메시지에서 감정/호감도 트리거를 감지하는 클래스"""
    
    def __init__(self):
        self.setup_patterns()
    
    def setup_patterns(self):
        """감지 패턴들을 초기화합니다"""
        
        # 감정 트리거 패턴
        self.emotion_patterns = {
            "수줍음": [
                r"부끄러|수줍|부끄|숨고싶|얼굴이빨개|부끄러워",
                r"창피|민망|부끄러움"
            ],
            "기쁨": [
                r"기쁘|좋아|행복|즐거|신나|웃음|하하|히히|ㅋㅋ|ㅎㅎ",
                r"최고|완전|대박|굉장|좋네|멋지|예뻐|사랑해"
            ],
            "슬픔": [
                r"슬프|우울|눈물|울|힘들|외로|아프|상처|속상|마음이",
                r"ㅠㅠ|ㅜㅜ|흑흑|안좋|걱정"
            ],
            "화남": [
                r"화나|짜증|분노|열받|빡치|뭐야|이상해|싫어|최악|별로",
                r"그만|하지마|안해|기분나쁘"
            ],
            "놀람": [
                r"어|헉|와|우와|대박|놀라|진짜|정말|어떻게|믿을수없|신기|wow",
                r"어머|깜짝|놀랐"
            ],
            "설렘": [
                r"설레|두근|심장|떨려|기대|멋져|예뻐|좋아해|사랑|로맨틱",
                r"달콤|따뜻|포근|특별|소중"
            ]
        }
        
        # 호감도 증가 트리거 패턴
        self.positive_affection_patterns = {
            "compliment": [
                r"예뻐|이쁘|귀여|멋져|좋아|사랑해|완벽|최고|대단|훌륭",
                r"멋있|아름다|매력|특별|소중|따뜻|친절|착해"
            ],
            "remember_details": [
                r"기억|생각|알아|저번에|전에 말한|말했던|얘기했던",
                r"카오루코|와구리|17살|고등학생|다도부"
            ],
            "romantic_gesture": [
                r"사랑|데이트|만나|보고싶|그리워|함께|같이|키스|포옹|안아",
                r"선물|꽃|반지|목걸이|편지"
            ],
            "gift_mention": [
                r"선물|줄게|사줄|받아|드릴|가져다|챙겨|준비했",
                r"꽃|케이크|초콜릿|반지|목걸이|인형|책"
            ],
            "daily_chat": [
                r"안녕|좋은아침|잠깐|하루|오늘|어떻게|지내|인사",
                r"일어났어|자러가|굿나잇|잘자|또봐"
            ]
        }
        
        # 호감도 감소 트리거 패턴
        self.negative_affection_patterns = {
            "rude_behavior": [
                r"바보|멍청|짜증|꺼져|닥쳐|시끄러|죽어|미워|싫어|최악",
                r"못생|더러|추해|별로|그만|하지마"
            ],
            "inappropriate_content": [
                r"섹스|야동|19금|음란|변태|몸|가슴|다리|속옷",
                r"벗어|만져|키스해|자자|침대|모텔"
            ],
            "harsh_words": [
                r"실망|화나|짜증나|상처|아프게|슬프게|기분나쁘",
                r"왜그래|이상해|문제|틀렸|잘못"
            ]
        }
        
        # 특수 상황 패턴
        self.special_patterns = {
            "long_conversation": None,  # 시간 기반으로 판단
            "ignore_long_time": None,   # 마지막 대화 시간 기반
            "special_occasion": [
                r"생일|크리스마스|발렌타인|화이트데이|새해|졸업|입학|시험",
                r"축하|기념일|특별한날|중요한날"
            ]
        }
    
    def analyze_message(self, message: str, user_name: str, 
                       conversation_start_time: datetime, 
                       last_interaction_time: Optional[datetime] = None) -> Dict:
        """
        메시지를 분석해서 트리거들을 찾습니다
        
        Returns:
            {
                "emotion_triggers": [("emotion_name", confidence), ...],
                "affection_triggers": [("trigger_name", multiplier), ...],
                "conversation_length": minutes,
                "special_context": {...}
            }
        """
        
        result = {
            "emotion_triggers": [],
            "affection_triggers": [],
            "conversation_length": 0,
            "special_context": {}
        }
        
        message_lower = message.lower()
        
        # 1. 감정 트리거 분석
        result["emotion_triggers"] = self._detect_emotion_triggers(message_lower)
        
        # 2. 호감도 트리거 분석
        result["affection_triggers"] = self._detect_affection_triggers(message_lower)
        
        # 3. 대화 길이 계산
        result["conversation_length"] = self._calculate_conversation_length(
            conversation_start_time
        )
        
        # 4. 장기간 무시 체크
        if last_interaction_time:
            result["ignore_duration"] = self._check_ignore_duration(last_interaction_time)
        
        # 5. 특별한 상황 체크
        result["special_context"] = self._detect_special_context(message_lower)
        
        return result
    
    def _detect_emotion_triggers(self, message: str) -> List[Tuple[str, float]]:
        """감정 트리거를 감지합니다"""
        detected_emotions = []
        
        for emotion, patterns in self.emotion_patterns.items():
            confidence = 0.0
            
            for pattern in patterns:
                matches = re.findall(pattern, message)
                if matches:
                    # 매치 횟수와 길이에 따라 신뢰도 계산
                    confidence += len(matches) * 0.3
            
            # 특정 키워드 조합으로 신뢰도 조정
            if emotion == "기쁨":
                if any(word in message for word in ["정말", "너무", "완전"]):
                    confidence *= 1.5
            elif emotion == "슬픔":
                if any(word in message for word in ["많이", "너무", "정말"]):
                    confidence *= 1.5
            
            # 신뢰도가 일정 수준 이상이면 추가
            if confidence >= 0.3:
                detected_emotions.append((emotion, min(confidence, 1.0)))
        
        # 신뢰도 순으로 정렬
        detected_emotions.sort(key=lambda x: x[1], reverse=True)
        return detected_emotions[:2]  # 최대 2개까지
    
    def _detect_affection_triggers(self, message: str) -> List[Tuple[str, float]]:
        """호감도 트리거를 감지합니다"""
        detected_triggers = []
        
        # 긍정적 트리거 체크
        for trigger, patterns in self.positive_affection_patterns.items():
            if patterns:
                for pattern in patterns:
                    if re.search(pattern, message):
                        multiplier = 1.0
                        
                        # 강조 표현에 따른 배수 조정
                        if any(word in message for word in ["정말", "너무", "완전", "진짜"]):
                            multiplier = 1.5
                        elif any(word in message for word in ["좀", "조금", "약간"]):
                            multiplier = 0.8
                        
                        detected_triggers.append((trigger, multiplier))
                        break
        
        # 부정적 트리거 체크
        for trigger, patterns in self.negative_affection_patterns.items():
            if patterns:
                for pattern in patterns:
                    if re.search(pattern, message):
                        multiplier = 1.0
                        
                        # 강한 부정 표현 체크
                        if any(word in message for word in ["진짜", "정말", "완전", "너무"]):
                            multiplier = 1.5
                        
                        detected_triggers.append((trigger, multiplier))
                        break
        
        return detected_triggers
    
    def _calculate_conversation_length(self, start_time: datetime) -> int:
        """대화 지속 시간을 분 단위로 계산합니다"""
        duration = datetime.now() - start_time
        return int(duration.total_seconds() / 60)
    
    def _check_ignore_duration(self, last_interaction: datetime) -> int:
        """마지막 상호작용 이후 경과 시간을 시간 단위로 계산합니다"""
        duration = datetime.now() - last_interaction
        return int(duration.total_seconds() / 3600)  # 시간 단위
    
    def _detect_special_context(self, message: str) -> Dict:
        """특별한 상황을 감지합니다"""
        special_context = {}
        
        # 특별한 날 언급 체크
        for pattern in self.special_patterns["special_occasion"]:
            if re.search(pattern, message):
                special_context["special_occasion"] = True
                break
        
        # 첫 만남인지 체크
        if any(word in message for word in ["처음", "첫", "안녕하세요", "반가워"]):
            special_context["first_meeting"] = True
        
        # 작별 인사 체크
        if any(word in message for word in ["안녕", "잘가", "나중에", "또봐", "굿바이"]):
            special_context["goodbye"] = True
        
        # 질문 패턴 체크
        if any(char in message for char in ["?", "？"]) or any(word in message for word in ["뭐", "어떻게", "왜", "언제", "어디"]):
            special_context["question"] = True
        
        return special_context
    
    def get_conversation_bonus_multiplier(self, conversation_length: int) -> float:
        """대화 길이에 따른 보너스 배수를 반환합니다"""
        if conversation_length >= 30:  # 30분 이상
            return 2.0
        elif conversation_length >= 15:  # 15분 이상
            return 1.5
        elif conversation_length >= 5:   # 5분 이상
            return 1.2
        else:
            return 1.0
    
    def should_apply_ignore_penalty(self, ignore_duration: int) -> bool:
        """무시 패널티를 적용해야 하는지 판단합니다"""
        return ignore_duration >= 24  # 24시간 이상
    
    def get_context_emotion_modifier(self, special_context: Dict) -> Dict[str, float]:
        """특별한 상황에 따른 감정 수정자를 반환합니다"""
        modifiers = {}
        
        if special_context.get("first_meeting"):
            modifiers["수줍음"] = 1.5
            modifiers["놀람"] = 1.2
        
        if special_context.get("goodbye"):
            modifiers["슬픔"] = 1.3
            modifiers["기쁨"] = 0.8
        
        if special_context.get("special_occasion"):
            modifiers["기쁨"] = 1.5
            modifiers["설렘"] = 1.3
        
        return modifiers