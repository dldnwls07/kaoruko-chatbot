"""
감정 시스템 1단계 테스트 스크립트
각 클래스의 기본 기능들을 테스트합니다.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from emotion_system import EmotionManager, AffectionManager, ResponseGenerator, TriggerDetector
from datetime import datetime, date

def test_emotion_manager():
    """EmotionManager 기본 기능 테스트"""
    print("🧪 EmotionManager 테스트 시작...")
    
    try:
        # 가상 DB 세션 (실제 DB 없이 테스트)
        emotion_manager = EmotionManager(None)  # db=None으로 테스트
        
        # 1. 감정 초기화 테스트
        print("  ✅ EmotionManager 인스턴스 생성 성공")
        
        # 2. 감정 전환 규칙 테스트 (모듈 레벨 import)
        from emotion_system.emotion_manager import EMOTION_TRANSITIONS, EMOTIONS
        print(f"  ✅ 감정 전환 규칙 개수: {len(EMOTION_TRANSITIONS)}")
        
        # 3. 감정 목록 확인
        emotions = list(EMOTIONS.keys())
        print(f"  ✅ 지원 감정 목록: {emotions}")
        
        # 4. 감정 응답 테스트
        response = emotion_manager.get_emotion_response("기쁨", 0.7)
        print(f"  ✅ 감정 응답 생성: {response[:20]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ EmotionManager 테스트 실패: {e}")
        return False

def test_affection_manager():
    """AffectionManager 기본 기능 테스트"""
    print("\n🧪 AffectionManager 테스트 시작...")
    
    try:
        affection_manager = AffectionManager(None)  # db=None으로 테스트
        
        # 1. 관계 단계 확인
        stage = affection_manager.get_relationship_stage(25)
        print(f"  ✅ 호감도 25 → 관계 단계: {stage}")
        
        # 2. 호감도 변화 계산 (모듈 레벨 import)
        from emotion_system.affection_manager import AFFECTION_TRIGGERS
        base_change = AFFECTION_TRIGGERS.get("compliment", 0)
        print(f"  ✅ 칭찬 트리거 호감도 변화: {base_change}")
        
        # 3. 호칭 시스템 테스트
        title = affection_manager.get_title_for_user("테스트", 75)
        print(f"  ✅ 호감도 75일 때 호칭: {title}")
        
        # 4. 진행률 계산
        progress = affection_manager.get_affection_progress_percentage(45)
        print(f"  ✅ 호감도 45 진행률: {progress}%")
        
        return True
        
    except Exception as e:
        print(f"  ❌ AffectionManager 테스트 실패: {e}")
        return False

def test_trigger_detector():
    """TriggerDetector 기본 기능 테스트"""
    print("\n🧪 TriggerDetector 테스트 시작...")
    
    try:
        detector = TriggerDetector()
        
        # 1. 감정 트리거 감지 테스트
        emotions = detector._detect_emotion_triggers("정말 기뻐요! 너무 좋아요!")
        print(f"  ✅ 감정 트리거 감지: {emotions}")
        
        # 2. 호감도 트리거 감지 테스트  
        affection = detector._detect_affection_triggers("카오루코 정말 예뻐요!")
        print(f"  ✅ 호감도 트리거 감지: {affection}")
        
        # 3. 특별 상황 감지 테스트
        context = detector._detect_special_context("처음 만나서 반가워요!")
        print(f"  ✅ 특별 상황 감지: {context}")
        
        # 4. 대화 길이 계산 테스트
        start_time = datetime.now()
        length = detector._calculate_conversation_length(start_time)
        print(f"  ✅ 대화 길이 계산: {length}분")
        
        return True
        
    except Exception as e:
        print(f"  ❌ TriggerDetector 테스트 실패: {e}")
        return False

def test_response_generator():
    """ResponseGenerator 기본 기능 테스트"""
    print("\n🧪 ResponseGenerator 테스트 시작...")
    
    try:
        generator = ResponseGenerator()
        
        # 1. 감정별 스타일 확인
        emotion_style = generator.emotion_styles.get("수줍음", {})
        print(f"  ✅ 수줍음 감정 스타일: {emotion_style.get('tone', '')}")
        
        # 2. 호감도별 스타일 확인
        affection_style = generator.affection_styles.get("친구", {})
        print(f"  ✅ 친구 단계 말투: {affection_style.get('speech_level', '')}")
        
        # 3. 이모티콘 매핑 테스트
        emoji = generator.get_emotion_display_emoji("기쁨")
        print(f"  ✅ 기쁨 감정 이모티콘: {emoji}")
        
        # 4. 호감도 표시 정보 테스트
        display_info = generator.get_affection_display_info(65, "절친")
        print(f"  ✅ 호감도 65 표시 정보: {display_info}")
        
        # 5. 시스템 메시지 생성 테스트
        level_up_msg = generator.generate_system_message("level_up", new_stage="친구")
        print(f"  ✅ 레벨업 메시지: {level_up_msg}")
        
        return True
        
    except Exception as e:
        print(f"  ❌ ResponseGenerator 테스트 실패: {e}")
        return False

def main():
    """전체 테스트 실행"""
    print("🚀 감정 시스템 1단계 테스트 시작\n")
    
    results = []
    
    # 각 클래스별 테스트 실행
    results.append(test_emotion_manager())
    results.append(test_affection_manager())
    results.append(test_trigger_detector()) 
    results.append(test_response_generator())
    
    # 결과 요약
    print("\n" + "="*50)
    print("📊 테스트 결과 요약")
    print("="*50)
    
    success_count = sum(results)
    total_count = len(results)
    
    if success_count == total_count:
        print("🎉 모든 테스트 통과!")
        print("✨ 1단계 감정 시스템이 정상적으로 구현되었습니다!")
    else:
        print(f"⚠️  {total_count - success_count}/{total_count} 테스트 실패")
        print("🔧 실패한 부분을 수정해야 합니다.")
    
    print(f"\n성공률: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")

if __name__ == "__main__":
    main()